'''
Description: Automation of the cello python API and display the results of 
usuage -- python automateAPI.py

################################################################################

Test Procedure:

Step One:
1) Get ucf file name that is in working directory
2) Run exclude_data.py to get rid of flow cytometry data
3) Post ucf file to Cello
4) Assign random JobID to user
5) Submit job with original ucf file
6) Get results of job and read in original circuit score

Step Two:
1) Take original submitted ucf file
2) Run bio.py to do protein engineering
3) Submit job with new ucf file, but same verilog and inputs/outputs
4) Get results of job and record new circuit score
5) Try doing DNA engineering iteratively to improve circuit score 
6) Calculate the percentage increase of circuit score and display

################################################################################

Methods:

get_ucf_name: searchs contents of working directory for name of present ucf file
get_verilog_name: search contents of working directory for name of present verilog file
jobID: generates random job ID number to be used
post_ucf: automatically posts ucf file to cello
exclude_data: runs python script to remove flow cytometry data from ucf file
protein_eng: runs python script to improve ucf file
submit_job: automatically submits job with desired inputs
get_results: returns circuit score of submitted job
calculate_score_increase: returns percentage increase in score after running step two

'''

import re
import os
import sys
import subprocess
import random
import time

######################################## DEFINE ALL POSSIBLE GATES ########################################################

gates = ["A1_AmtR", "B1_BM3R1", "B2_BM3R1","B3_BM3R1","E1_BetI",\
        "F1_AmeR","H1_HlyIIR","I1_IcaRA","L1_LitR", "N1_LmrA", "P1_PhlF",\
        "P2_PhlF", "P3_PhlF", "Q1_QacR","Q2_QacR","R1_PsrA","S1_SrpR", \
        "S2_SrpR","S3_SrpR","S4_SrpR"]


########################################## DEFINE PRANAY CLASS ############################################################

class PRANAY:

    def __init__(self):
        print "initializing new pranay object.....\n"

    def get_ucf_name(self):
        try:
            proc = subprocess.Popen('ls',stdout = subprocess.PIPE)
        except OSError, ValueError:
            print "OS exception getting ucf file name"
            return "Fail"
        out, err = proc.communicate()
        for line in re.split("\n",str(out)):
            if "UCF.json" in line:
                return line

    def get_verilog_name(self):
        try:
            proc = subprocess.Popen(['ls'], stdout = subprocess.PIPE)
        except OSError, ValueError:
            print "OS exception getting verilog file name"
        out, err = proc.communicate()
        for line in re.split("\n",str(out)):
            if "vhdl" in line:
                return line


    def jobID(self):
        return "job" + str(random.randrange(1,1000))

    def post_ucf(self, ucf):
        try:
            proc = subprocess.Popen(['python', 'cello_client.py', 'post_ucf', \
                                    '--name', str(ucf), '--filepath', str(ucf)], stdout = subprocess.PIPE)
        except OSError, ValueError:
            print "could not post ucf"
        out, err = proc.communicate()
        lines = re.split("\n", str(out))
        for line in lines:
            if "200" in line:
                return "Pass"

    def exclude_data(self, filename):
        try:
            proc = subprocess.Popen(['python', 'exclude_data.py', filename], stderr = subprocess.PIPE)
        except OSError, ValueError:
            print "OS Error running exclude_data.py"

    def protein_eng(self, ucf, gate_name, protein = 1, dna = None ):
        try:
            proc = subprocess.Popen(['python', 'bio.py', ucf, str(gate_name), str(protein), str(dna)])
        except OSError, ValueError:
            print "...Error doing protein engineering..."

    def submit_job(self, jobID,verilog,inputs,outputs,ucf):
        try:
            proc = subprocess.Popen(['python', 'cello_client.py', 'submit', '--jobid', str(jobID), '--verilog', verilog, \
                                    '--inputs', str(inputs), '--outputs', str(outputs), \
                                    '--options=-UCF Original.UCF.json -plasmid false -eugene false'], stdout = subprocess.PIPE)
        except OSError, ValueError:
            print "...Error while submitting job..."
            return "Fail"
        out, err = proc.communicate()
        for line in re.split("\n",str(out)):
            if re.search('200',line):
                return "Pass"
    def get_results(self, jobID):
        try:
            proc = subprocess.Popen(['python', 'cello_client.py', 'get_results', '--jobid',str(jobID), \
                                    '--filename',str(jobID)+'_dnacompiler_output.txt'], stdout = subprocess.PIPE)
        except OSError, ValueError:
            print "...Error while getting results..."
        out, err = proc.communicate()
        for line in re.split("\n",str(out)):
            if "Circuit_score" in line:
                score = re.split(" ",line)
        stop = False
        for line in re.split("\n", str(out)):
            if "Gate=" in line:
                for gate in gates:
                    if gate in line and not stop:
                        gate_name = re.split(" ", line)[0]
                        stop = True
        return score[2], gate_name #return Circuit_score

    def calculate_score_increase(self, oldScore, newScore):
        increase = (float(newScore) - float(oldScore))/float(oldScore)
        increase = increase * 100
        return increase


###############################################INITIALIZE TEST################################################################


'''Step One'''
princess = PRANAY()
# t0 = time()
results = []
ucf_file = princess.get_ucf_name()
princess.exclude_data(ucf_file)
jobID = princess.jobID()
print jobID + '...'
result = princess.post_ucf(ucf_file)
if result is not "Pass":
    print "couldnt post ucf"
else:
    print "posted ucf"
#hard code these file values for now will add more to api later
inputs = "Inputs.txt"
outputs = "Outputs.txt"
verilog = princess.get_verilog_name()
submit = princess.submit_job(jobID,verilog,inputs,outputs,ucf_file)
if submit is "Pass":
    gate_name = []
    oldScore, gate_name = princess.get_results(jobID)
    results.append(float(oldScore))
    if oldScore is None:
        print "couldnt get results of Step One"
    else:
        stepOne = "Pass"
else:
    print "couldnt submit job"

'''Step Two'''
if stepOne is "Pass":
    princess.protein_eng(ucf_file, gate_name)
    result = princess.post_ucf(ucf_file)
    submit = princess.submit_job(str(jobID),verilog,inputs,outputs,ucf_file)
    newScore, gate_name = princess.get_results(jobID)
    results.append(float(newScore))
    highest = False
    i = 1
    while not highest:
        if results[i-1] >= results[i]:
            highest = True
            newScore = results[i-1] #highest score
        else:
            princess.protein_eng(ucf_file, gate_name, protein = 0, dna = 1/(i*2.5))
            submit = princess.submit_job(jobID,verilog,inputs,outputs,ucf_file)
            newScore, gate_name = princess.get_results(jobID)
            results.append(float(newScore))
            i += 1

    result = princess.calculate_score_increase(oldScore,newScore)
    oldScore = '%.2f' % round(float(oldScore), 2)
    newScore = '%.2f' % round(float(newScore), 2)
    result = '%.2f' % round(result, 2) #round result to two decimal placess
    print("...The original circuit score was %s, after running Jello it is now... %s" % (oldScore, newScore))
    print("...percentage increase is: %s percent for job:... %s" % (str(result), jobID))
    print("....percentage increase is: %s percent...." % str(result))
    # print("done in %.3fs"%(time()-t0))

################################################## TEST COMPLETE #############################################################