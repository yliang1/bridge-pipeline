# runPulsarAnalysis.py
#
# IMPORTANT:
#   call this script like this: 
#	python runBridgeAnalysis --pulsar J1918 --dataset nanograv5 -s ####
#
#
import argparse
from subprocess import Popen, PIPE

wmgr_client_path = '/Users/skhudiky/workspace/Nano-code/nanograv-pipeline/workflow/bin/wmgr-client'
#wmgr_client_path = '/usr/local/nanograv-pipeline/workflow/bin/wmgr-client'


parser = argparse.ArgumentParser(description='Process pulsar analysis.')
#parser.add_argument('--pulsar',  type=str, dest='pulsars', required=True, help='names of pulsars to use')
parser.add_argument('--dataset', type=str, dest='dataset', required=True, help='directory name for specified pulsar')
parser.add_argument('-s', '--temp_session', type=int, 	help='a temporary session id to keep track of user data (value ranges 10000:99999; default: 12345)', default="12345")


# Set arguments to appropriate variable
args = parser.parse_args()
#str_list = args.pulsars.split(',')
#pulsars = filter(None, str_list)
dataset = args.dataset

# Get temporary session id to keep track of what data belongs to what run
temp_session = args.temp_session
if not (temp_session) : temp_session = '12345'


# Loop through list of pulsars to send event to run workflow
#for pulsar in pulsars :
	# Set the command to run with all parameters
command = [ wmgr_client_path
		,'--url' ,'http://localhost:9103' ,'--operation' ,'--sendEvent' 
		,'--eventName' ,'FStat_Event' ,'--metaData'
#		,'--key' ,'PULSAR' , pulsar
		,'--key' ,'DATASET' , dataset
		,'--key' ,'TEMP_SESSION' , str(temp_session)
	]
# command += other_keys
output = Popen(command, stdout=PIPE, stderr=PIPE)
stdout, stderr = output.communicate()
if stdout.find('error') > 0 :
	print stdout.find('error')
	# break

print temp_session
