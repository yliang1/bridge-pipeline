# filterTOA.py
#
# This script runs filtering on TOA files and makes sure that the pipeline is handed 
# the proper file to continue with analysis
#
# IMPORTANT:
#   call this script like this: python filterTOA --toa /full/path/to/pulsar.tim 
# 		-ot /full/path/to/output/file -st #### -et #### -sf #### -ef ####
#
import argparse
import shutil
from subprocess import Popen, PIPE

# TODO set these in a config 
bridge_TimeFilterPath = '/Users/skhudiky/workspace/Nano-code/nanograv-pipeline/pge/bin/bridge/filtering-libstempo/TOA_Filtering.py'
bridge_FreqFilterPath = '/Users/skhudiky/workspace/Nano-code/nanograv-pipeline/pge/bin/bridge/filtering-libstempo/Frequency_Filtering.py'
# Operational
# bridge_TimeFilterPath = '/usr/local/nanograv-pipeline/pge/bin/bridge/filtering-libstempo/TOA_Filtering.py'
# bridge_FreqFilterPath = '/usr/local/nanograv-pipeline/pge/bin/bridge/filtering-libstempo/Frequency_Filtering.py'


parser = argparse.ArgumentParser(description='Filter TOA with time and frequency range.')
# parser.add_argument('-time', '--bridge_TimeFilterPath', help='The full path to the time range filter script')
# parser.add_argument('-freq', '--bridge_FreqFilterPath', help='The full path to the frequency range filter script')
parser.add_argument('-toa',	'--toa_file', help='the path to the raw TOA to filter')
parser.add_argument('-par',	'--par_file', help='the path to the raw par file')
parser.add_argument('-ot',	'--output_tim', help='The full path to the out TOA file')
parser.add_argument('-st',	'--start_time_filter', type=int, help='start time for filtering')
parser.add_argument('-et',	'--end_time_filter', type=int, help='end time for filtering')
parser.add_argument('-sf',	'--start_frequency_filter', type=float, help='start frequency for filtering')
parser.add_argument('-ef',	'--end_frequency_filter', type=float, help='end frequency for filtering')

# Set arguments to appropriate variable
args = parser.parse_args()
# bridge_TimeFilterPath = args.bridge_TimeFilterPath
# bridge_FreqFilterPath = args.bridge_FreqFilterPath
toa_file = args.toa_file
par_file = args.par_file
start_time_filter = args.start_time_filter
end_time_filter = args.end_time_filter
start_frequency_filter = args.start_frequency_filter
end_frequency_filter = args.end_frequency_filter

# Set the command to run with all parameters and set the output to output_tim
output_tim = args.output_tim
command = ''
print toa_file
# If time filter is set, run bridge_TimeFilterPath script
if (start_time_filter and end_time_filter ) :
	command = [ 'python', bridge_TimeFilterPath,
		par_file, toa_file,  
		str(start_time_filter), str(end_time_filter), output_tim]
	output = Popen(command, stdout=PIPE, stderr=PIPE)
	stdout, stderr = output.communicate()
	if not stderr :
		toa_file = output_tim
 
# If frequency filter is set, run bridge_FreqFilterPath script
if (start_frequency_filter and end_frequency_filter) :
	command = [ 'python', bridge_FreqFilterPath,
		par_file, toa_file,  
		str(start_frequency_filter), str(end_frequency_filter), output_tim]

print toa_file

if not (command) :
	shutil.copy(toa_file, output_tim)
	print output_tim
else :
	output = Popen(command, stdout=PIPE, stderr=PIPE)
	stdout, stderr = output.communicate()
	if (stderr) :
		print stderr
	else :
		print output_tim


