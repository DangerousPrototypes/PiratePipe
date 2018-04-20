import sys
import subprocess
import json
import time
import os
import argparse
import base64
import requests
import imp
from pprint import pprint


parser = argparse.ArgumentParser(description='Dangerous Prototypes auto build v2.0')
parser.add_argument('--tasks', required=False, default='buildv2_tasks.py', help='Build tasks configuration file')
parser.add_argument('--interval', required=False, default='10', help='Repeat interval in minutes')
parser.add_argument('--test', required=False, default=False, help='Run in test mode')

args = vars(parser.parse_args())
#pprint(args)

class autoBuild:
	def __init__(self):
		#import make tasks config
		with open(args['tasks'],'r') as infile:
			tasks=imp.load_source( 'tasks', '',infile) 
		self.tasks=tasks.tasks
		
	def runTasks(self):
		for task in self.tasks:
			#self.make(task)
			pprint(task)
			pprint(task['work_dir'])
	
	def make(self, task):
		timestampstart=time.time()

		#git log --pretty=format:'%h' -n 1 #or H for long hash
		hashshort = subprocess.check_output('cd '+task['work_dir']+" && git log --pretty=format:'%h' -n 1",shell=True).decode().strip("'")
		hashlong = subprocess.check_output('cd '+task['work_dir']+" && git log --pretty=format:'%H' -n 1",shell=True).decode().strip("'")


		gitoutput=subprocess.check_output('cd '+task['work_dir']+' && git pull',shell=True).decode()

		newhashshort = subprocess.check_output('cd '+task['work_dir']+" && git log --pretty=format:'%h' -n 1",shell=True).decode().strip("'")
		newhashlong = subprocess.check_output('cd '+task['work_dir']+" && git log --pretty=format:'%H' -n 1",shell=True).decode().strip("'")

		print(hashlong)
		print(gitoutput)
		print(newhashlong)
		result={}
		if args['test'] is not False or hashlong != newhashlong:
			print('Preparing build report')
			subprocess.check_output('cd '+task['work_dir']+' && make clean', shell=True)
			try:
				makeoutput=subprocess.check_output('cd '+task['work_dir']+' && '+task['make_command'], shell=True,stderr=subprocess.STDOUT).decode()
				result['error']='0';
			except subprocess.CalledProcessError as e:
				#print("command '"+e.cmd+"' return with error (code "+e.returncode.decode()+"): "+e.output)	
				pprint(e.returncode)
				#pprint(stderr)
				makeoutput=str(e.output.decode())
				result['error']='1'
				pprint(makeoutput)

			#create data structure
			result['timestamp']={}
			result['timestamp']['start']=timestampstart
			result['timestamp']['stop']=time.time()
			result['firmware']=task['firmware']
			result['hardware']=task['hardware']
			result['starthashshort']=hashshort
			result['starthashlong']=hashlong
			result['endhashshort']=newhashshort
			result['endhashlong']=newhashlong
			result['gitoutput']=gitoutput
			result['makeoutput']=makeoutput
			result['apikey']=task['api_key']
			result['response']='json'
			result['firmware_type']=task['output_file'].split(".")[-1] 	

			#base64 encode file
			if os.path.exists(task['output_dir'] + '/' + task['output_file']):
				print('Base 64 encoding file')
				with open(task['output_dir'] + '/' + task['output_file'], "rb") as firmware: 
					result['base64encbin']= base64.b64encode(firmware.read()).decode()

			#upload .json to API
			print("Dumping JSON")	
			with open(task['work_dir'] + '/result.json', 'w') as outfile:
				json.dump(result, outfile, indent=4, sort_keys=False)
				
			print("Uploading JSON")
			with open(task['work_dir'] + '/result.json', 'rb') as f: 
				r = requests.post(task['api_url'], files={'result': f})	
			pprint(r)
			pprint(r.text)
			subprocess.check_output('cd '+task['work_dir']+' && make clean', shell=True)

ab=autoBuild()

while(True):
	ab.runTasks();
	print('sleep')
	#sleep for configured number of minutes
	time.sleep(args['interval']*60)



