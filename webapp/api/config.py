
''' Configuration settings for the Bridge backend webservices. '''

# Parent directory that the frontend is allowed to load files from.
# Any directory under this will be visible to the frontend.
ARCHIVE_PATH_LEADER = '/Users/skhudiky/workspace/Nano-code/nanograv-pipeline/data/archive/'
JOBS_PATH_LEADER = '/Users/skhudiky/workspace/Nano-code/nanograv-pipeline/data/jobs/'

# Path to the python script for starting residual plotting workflow
RES_SCRIPT = '/Users/skhudiky/workspace/Nano-code/nanograv-pipeline/pge/bin/runPulsarAnalysis.py'
OS_SCRIPT = '/Users/skhudiky/workspace/Nano-code/nanograv-pipeline/pge/bin/runBridgeAnalysis.py'
FSTAT_SCRIPT = '/Users/skhudiky/workspace/Nano-code/nanograv-pipeline/pge/bin/runFstatAnalysis.py'