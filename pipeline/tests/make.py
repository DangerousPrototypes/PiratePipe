import json
import os
import glob
import argparse
import imp
from pprint import pprint
from os.path import basename

parser = argparse.ArgumentParser(description='Bus Pirate Test Script Make v1.0')
parser.add_argument('--test', required=False, default='.', help='Test script (folder) to load')

class makeTestJSON:
	def make(filename):
		if basename(filename) == 'make.py': #skip self
			return;
		else:
			print(filename)
			
		with open(filename,'r') as infile:
			test=imp.load_source( 'test', '',infile) 
		
		#pprint(test.test)
		
		json_filename=os.path.splitext(filename)[0]+'.json'
		
		print(json_filename)
		with open(json_filename, 'w') as outfile:
			json.dump(test.test, outfile, indent=4, sort_keys=False)

args = vars(parser.parse_args())

make=makeTestJSON;

#are we loading a single script or a folder of scripts?
if os.path.isfile(args['test']):
	make.make(args['test'])
elif os.path.isdir(args['test']):
	for filename in glob.glob(os.path.join(args['test'], '*.py')):
		make.make(filename)