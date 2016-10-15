'''
Description: Make modifications to input UCF file to improve circuit score
usuage -- python bio.py UCF.json gate_name protein dna

################################################################################

Test Procedure:

1) Take a ucf file, protein eng, dna eng multplier and gate to do dna eng on as args
if protein is 1 then:
    2) Multiply ymax value response_functions collection by 1.5
    3) Divide ymin value response_functions collection by 1.5
    4) Multiply n value response_functions collection by 1.05 to increase slope
    5) Show resulting modified data
elif protein is 0 then:
    6) Use strong_rbs method to multiple "K" value by specified number
    7) Store resulting Data

################################################################################

Methods:

load_file: loads ucf file given in argument
multiply: multiplies all ymax values by N to strecth resp function
increase_slope: increases slope of response function
divide: divides all ymin values by N to strecth resp function
show_data: prints contents of each gate response function parameters
modify: allows user to modify all values at once by single input N
strong_rbs: multiplies K value of given gate s
store: stores modified json file

'''

import json
import sys
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="path to UCF.json file")
parser.add_argument("gate_name", nargs = '*',help="name of gate to do operations on")
parser.add_argument("protein", help = "1 if protein engineering 0 if not", type = int)
parser.add_argument("dna", help="Number by which to strenghthen or weaken rbs", type=None)
args = vars(parser.parse_args())

filepath = args.get("filepath", None)
protein = args.get("protein", None)
dna = args.get("dna", None)
gate_name = args.get("gate_name", None)



class JSON:
    # filepath = sys.argv[1]

    def __init__(self):
        print "\nInitialized new object.......\n"

    def loadfile(self):
        with open(filepath) as data_file:
            self.data = json.load(data_file)
        print "\nLoaded file into object.......\n"

    def multiply(self, N):  # modify ymax
        for objects in self.data:
            if objects["collection"] == "response_functions":
                objects["parameters"][0]["value"] = N * float(objects["parameters"][0]["value"])

    def increase_slope(self, N):
        for objects in self.data:
            if objects["collection"] == "response_functions":
                objects["parameters"][3]["value"] = N * float(objects["parameters"][3]["value"])

    def divide(self, N):  # modify ymin and round to 3 decimal places
        for objects in self.data:
            if objects["collection"] == "response_functions":
                objects["parameters"][1]["value"] = float(objects["parameters"][1]["value"]) / N

    def show_data(self):
        print "\nCurrent values in the JSON file are..........\n"

        for objects in self.data:
            if objects["collection"] == "response_functions":
                print "Gate Name : ", objects["gate_name"]
                print objects["parameters"][0]["name"], ":", objects["parameters"][0]["value"]
                print objects["parameters"][1]["name"], ":", objects["parameters"][1]["value"]
                print objects["parameters"][2]["name"], ":", objects["parameters"][2]["value"]
                print objects["parameters"][3]["name"], ":", objects["parameters"][3]["value"]

    def strong_rbs(self, N, gate_name):
        for objects in self.data:
            if objects["collection"] == "response_functions":
                if objects["gate_name"] == gate_name:
                    objects["parameters"][2]["value"] = N * float(objects["parameters"][2]["value"])

    def weak_promoter(self, N):
        for objects in self.data:
            if objects["collection"] == "response_functions":
                objects["parameters"][1]["value"] == float(objects["parameters"][1]["value"]) / N
                objects["parameters"][0]["value"] == float(objects["parameters"][0]["value"]) / N

    def strong_promoter(self, N):
        for objects in self.data:
            if objects["collection"] == "response_functions":
                objects["parameters"][1]["value"] == N * float(objects["parameters"][1]["value"])
                objects["parameters"][0]["value"] == N * float(objects["parameters"][0]["value"])

    def store(self):
        with open(filepath, "w") as outfile:
            json.dump(self.data, outfile, sort_keys=True, indent=2)


newjson = JSON()  # Instantiate the object
myfile = newjson.loadfile()
if protein == 1:
    newjson.multiply(1.5)
    newjson.divide(1.5)
    newjson.increase_slope(1.05)
    newjson.store()  # store the modified json

else:
    for gate in gate_name:
        print "...you are dna engineering... %s" % gate
        newjson.strong_rbs(float(dna), gate)
        newjson.store()  # store the modified json
