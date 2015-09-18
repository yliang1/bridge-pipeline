# runPulsarAnalysis.py
#
# IMPORTANT:
#   call this script like this: python runPulsarAnalysis J1918 --temp_session ####
#
#
import argparse
from subprocess import Popen, PIPE

wmgr_client_path = '/Users/skhudiky/workspace/Nano-code/nanograv-pipeline/workflow/bin/wmgr-client'

parser = argparse.ArgumentParser(description='Process pulsar analysis.')
parser.add_argument('--pulsar',		type=str,	dest='pulsars', required=True, help='names of pulsars to use')
parser.add_argument('--dataset',	type=str, dest='dataset', required=True, help='directory name for specified pulsar')
parser.add_argument('-s',	 '--temp_session', 	type=int, 	help='a temporary session id to keep track of user data (value ranges 10000:99999; default: 12345)', default="12345")
parser.add_argument('-rp', '--res_plot', 			type=bool, 	help='a boolean for displaying residual plots (default: True)', default="True")
parser.add_argument('-pt', '--pulsar_timing', type=bool, 	help='a boolean for displaying pulsar timing (default: False)', default="False")
# parser.add_argument('','--time_filter', help='boolean for time filtering')
parser.add_argument('-st', '--start_time_filter', 	type=int, help='start time for filtering')
parser.add_argument('-et', '--end_time_filter', 		type=int, help='end time for filtering')
# parser.add_argument('','--frequency_filter', help='boolean for frequency filtering')
parser.add_argument('-sf', '--start_frequency_filter',  type=float, help='start frequency for filtering')
parser.add_argument('-ef', '--end_frequency_filter',  	type=float, help='end frequency for filtering')

# Set arguments to appropriate variable
args = parser.parse_args()
str_list = args.pulsars.split(',')
pulsars = filter(None, str_list)
dataset = args.dataset
res_plot = args.res_plot
pulsar_timing = args.pulsar_timing
start_time_filter = args.start_time_filter
end_time_filter = args.end_time_filter
start_frequency_filter = args.start_frequency_filter
end_frequency_filter = args.end_frequency_filter

# Get temporary session id to keep track of what data belongs to what run
temp_session = args.temp_session
if not (temp_session) : temp_session = '12345'

# Gather other information to inject into command
other_keys = []
if (start_time_filter and end_time_filter ) :
	other_keys += ['--key' ,'StartTime' , str(start_time_filter)]
	other_keys += ['--key' ,'EndTime' 	, str(end_time_filter)]
else :
	other_keys += ['--key' ,'StartTime' , str(0)]
	other_keys += ['--key' ,'EndTime' 	, str(0)]

if (start_frequency_filter and end_frequency_filter) :
	other_keys += ['--key' ,'StartFrequency' , str(start_frequency_filter)]
	other_keys += ['--key' ,'EndFrequency' 	 , str(end_frequency_filter)]
else :
	other_keys += ['--key' ,'StartFrequency' , str(0)]
	other_keys += ['--key' ,'EndFrequency' 	 , str(0)]

if (res_plot) :
	other_keys += ['--key' ,'RESIDUAL' , str(res_plot)]

if (pulsar_timing) :
	other_keys += ['--key' ,'PUSLAR_TIMING' , str(pulsar_timing)]

# Loop through list of pulsars to send event to run workflow
for pulsar in pulsars :
	# Set the command to run with all parameters
	command = [ wmgr_client_path
			,'--url' ,'http://localhost:9103' ,'--operation' ,'--sendEvent' 
			,'--eventName' ,'ResidualPlotting_Event' ,'--metaData'
			,'--key' ,'PULSAR' , pulsar
			,'--key' ,'DATASET' , dataset
			,'--key' ,'TEMP_SESSION' , str(temp_session)
	  	# ,'--key' ,'PUSLAR_TIMING', 'true'
	  	,'--key' ,'PLOT_PAR', 'true'
		]
	command += other_keys
	output = Popen(command, stdout=PIPE, stderr=PIPE)
	stdout, stderr = output.communicate()
	if stdout.find('error') > 0 :
		print stdout.find('error')
		break


print temp_session


