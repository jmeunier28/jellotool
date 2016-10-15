'''
Description: modify json file to exclude flow cytometry data

'''

import json
import sys

filepath = sys.argv[1]
with open(filepath) as data_file:
	filejson = json.load(data_file)

ucf = []

for obj in filejson:
    if obj['collection'] != 'gate_cytometry':
        ucf.append(obj)

#print json.dumps(ucf, indent=2)

with open(filepath, "w") as outfile:
	json.dump(ucf,outfile, sort_keys = True, indent = 2)
