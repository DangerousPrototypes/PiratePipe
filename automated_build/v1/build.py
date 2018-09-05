import sys
import subprocess
import json
import time
import os
import argparse
import base64
import requests
from pprint import pprint


parser = argparse.ArgumentParser(description='Bus Pirate auto build v1.0')
parser.add_argument('--url', required=False, help='Upload URL')
parser.add_argument('--apikey', required=False, help='Upload API key')
parser.add_argument('--workdir', required=True, help='Working directory')
parser.add_argument('--bin', required=True, help='Binary to upload')
parser.add_argument('--test', required=False, default=False, help='Run in test mode')
parser.add_argument('--hardware', required=True, help='Hardware version')
parser.add_argument('--firmware', required=True, help='Firmware version')
parser.add_argument('--make', required=True, help='Make command')

args = vars(parser.parse_args())
#pprint(args)
while True:
	timestampstart=time.time()

	#git log --pretty=format:'%h' -n 1 #or H for long hash
	hashshort = subprocess.check_output('cd '+args['workdir']+" && git log --pretty=format:'%h' -n 1",shell=True).decode().strip("'")
	hashlong = subprocess.check_output('cd '+args['workdir']+" && git log --pretty=format:'%H' -n 1",shell=True).decode().strip("'")


	gitoutput=subprocess.check_output('cd '+args['workdir']+' && git pull',shell=True).decode()

	newhashshort = subprocess.check_output('cd '+args['workdir']+" && git log --pretty=format:'%h' -n 1",shell=True).decode().strip("'")
	newhashlong = subprocess.check_output('cd '+args['workdir']+" && git log --pretty=format:'%H' -n 1",shell=True).decode().strip("'")

	print(hashlong)
	print(gitoutput)
	print(newhashlong)
	result={}
	if args['test'] is not False or hashlong != newhashlong:
		print('Preparing build report')
		subprocess.check_output('cd '+args['workdir']+' && make clean', shell=True)
		try:
			makeoutput=subprocess.check_output('cd '+args['workdir']+' && '+args['make'], shell=True,stderr=subprocess.STDOUT).decode()
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
		result['firmware']=args['firmware']
		result['hardware']=args['hardware']
		result['starthashshort']=hashshort
		result['starthashlong']=hashlong
		result['endhashshort']=newhashshort
		result['endhashlong']=newhashlong
		result['gitoutput']=gitoutput
		result['makeoutput']=makeoutput
		result['apikey']=args['apikey']
		result['response']='json'
		result['firmware_type']=args['bin'].split(".")[-1] 	

		#base64 encode file
		if os.path.exists(args['workdir'] + '/' + args['bin']):
			print('Base 64 encoding file')
			with open(args['workdir'] + '/' + args['bin'], "rb") as firmware: #TODO check if exists
				result['base64encbin']= base64.b64encode(firmware.read()).decode()

		#upload .json to API
		print("Dumping JSON")	
		with open(args['workdir'] + '/result.json', 'w') as outfile:
			json.dump(result, outfile, indent=4, sort_keys=False)
			
		print("Uploading JSON")
		with open(args['workdir'] + '/result.json', 'rb') as f: 
			r = requests.post(args['url'], files={'result': f})	
		pprint(r)
		pprint(r.text)
		subprocess.check_output('cd '+args['workdir']+' && make clean', shell=True)

	print('sleep')
	#sleep for configured number of minutes
	time.sleep(60*10)



