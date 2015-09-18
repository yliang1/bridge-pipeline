import re
import os.path
import random, json
from flask import Flask, Response, jsonify
from config import ARCHIVE_PATH_LEADER, JOBS_PATH_LEADER, RES_SCRIPT, OS_SCRIPT, FSTAT_SCRIPT
from flask.ext.cors import CORS
from subprocess import Popen, PIPE

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
dataset = 'nanograv5'

@app.route('/api/', defaults={'path': ''})
@app.route('/api/<path:path>')
def get_resource(path): 
    complete_path = os.path.join(JOBS_PATH_LEADER, path)
    mimetype = get_mimetype(path)
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)

@app.route('/api/analysis/<formData>')
def engage_analysis_workflow(formData): 
    formObj = json.loads(formData)
    session_id = formObj['session_id']
    analysis = formObj['analysis']
    other_keys = []

    if analysis == 'OS':
        command = [ 'python' ,OS_SCRIPT
                # ,'--pulsar' ,str(pulsars)
                ,'--dataset' ,'nanograv5' 
                ,'-s' ,str(session_id)
            ]
    elif analysis == 'Fstat':
        command = [ 'python' ,FSTAT_SCRIPT
                # ,'--pulsar' ,str(pulsars)
                ,'--dataset' ,'nanograv5' 
                ,'-s' ,str(session_id)
            ]

    # print command
    output = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = output.communicate()
    if stderr :
        return "Error: " + stderr
    if stdout.find('error') :
        return stdout
    time.sleep(300)
    return str(session_id)

@app.route('/api/download/', defaults={'path': ''})
@app.route('/api/download/<path:path>')
def download_resource(path): 
    complete_path = os.path.join(JOBS_PATH_LEADER, path)
    mimetype = get_mimetype(path)
    content = get_file(complete_path)
    filename = os.path.basename(complete_path)
    return Response(content, mimetype=mimetype, 
        headers={'Content-Disposition': 'attachment; filename="'+filename+'"'})

@app.route('/api/engage/<formData>')
def engage_workflow(formData): 
    session_id = random.randrange(10000, 99999)
    formObj = json.loads(formData)

    other_keys = []
    if (formObj['timeFilter'] != 'fullTime') :
      other_keys += ['-st' ,formObj['timeStartFilter'] ]
      other_keys += ['-et' ,formObj['timeEndFilter'] ]

    if (formObj['frequencyFilter'] != 'fullFrequency') :
      other_keys += ['-sf' ,formObj['frequencyStartFilter'] ]
      other_keys += ['-ef' ,formObj['frequencyEndFilter'] ]

    if (formObj['residualPlotting']) :
        other_keys += ['-rp' ,formObj['residualPlotting'] ]
    else :
        other_keys += ['-rp' ,'True' ]

    if (formObj['pulsarTiming']) :
      other_keys += ['-pt' ,formObj['pulsarTiming'] ]
    else :
        other_keys += ['-pt' ,'False']

    command = ''
    dataset = formObj['dataset']
    if (formObj[dataset]) :

        pulsars = ''.join(map(lambda x: '%s,' % x, formObj[dataset]))
        command = [ 'python' ,RES_SCRIPT
            ,'--pulsar' ,str(pulsars)
            ,'--dataset' ,dataset 
            ,'-s' ,str(session_id)
        ]

        print command
        output = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = output.communicate()
        if stderr :
            return "Error: " + stderr
        if stdout.find('error') :
            return stdout
    time.sleep(200)
    return str(session_id)

@app.route('/api/get/plots', defaults={'session_id': '12345'})
@app.route('/api/get/plots/<session_id>')
def get_plots(session_id): 
    try:
        pulsar_plot_data=[]
        session_plots_dir = session_id+'/plots/'
        complete_path = _get_clean_directory_path(JOBS_PATH_LEADER, session_plots_dir)
        plot_dir_listing = os.listdir(complete_path)
        session_data_dir = session_id+'/session_data/'
        complete_path = _get_clean_directory_path(JOBS_PATH_LEADER, session_data_dir)
        data_dir_listing = os.listdir(complete_path)
        session_pulsar_data_dir = session_id+'/avg_epoch/'
        complete_path = _get_clean_directory_path(JOBS_PATH_LEADER, session_pulsar_data_dir)
        pulsar_data_listing = os.listdir(complete_path)
        for filename in pulsar_data_listing :
            data = {}
            if filename.endswith('.json'):
                with open(os.path.join(complete_path,filename)) as data_file:    
                    data = json.load(data_file)
                    pulsar_name =  filename.split('.json')[0]
                    data["pulsar"] = pulsar_name
                    plot_name = [x for x in plot_dir_listing if pulsar_name in x][0]
                    data['filename'] = session_plots_dir+plot_name
                    tim_name = [x for x in data_dir_listing if (pulsar_name in x and x.endswith('.tim') )][0]
                    data['timFile'] = session_data_dir+tim_name
                    par_name = [x for x in data_dir_listing if (pulsar_name in x and x.endswith('.par') )][0]
                    data['parFile'] = session_data_dir+par_name
                    res_name = [x for x in pulsar_data_listing if (pulsar_name in x and x.endswith('.tim') )][0]
                    data['residualFile'] = session_pulsar_data_dir + res_name
                    pulsar_plot_data.append(data)
    except:
        pass
    else:
        pass
    return jsonify({'plot_data':pulsar_plot_data})

@app.route('/api/get/analysis_data', defaults={'session_id': '12345','analysis':'OS'})
@app.route('/api/get/analysis_data/<session_data>')
def get_os(session_data): 
    try:
        os_path=[]
        data={}
        formObj = json.loads(session_data)
        session_id = formObj['session_id']
        if formObj['analysis'] == 'OS' :
            session_stat_dir = session_id+'/optimal_stat/'
        elif formObj['analysis'] == 'Fstat' :
            session_stat_dir = session_id+'/f_stat/'

        complete_path = _get_clean_directory_path(JOBS_PATH_LEADER, session_stat_dir)
        dir_listing = os.listdir(complete_path)
        for p in dir_listing :
            mimetype = get_mimetype(p)
            if (mimetype == "application/pdf") :
                os_path.append(session_stat_dir+p)
            elif (mimetype == "image/png") :
                os_path.append(session_stat_dir+p)
            elif (mimetype == "text/plain") :
                os_path.append(session_stat_dir+p)
            elif (mimetype == "application/json") :
                with open(os.path.join(complete_path,p)) as data_file: 
                    data = json.load(data_file)
    except:
        pass
    else:
        pass
    data['img_path'] = os_path
    return jsonify({'analysis_data':data})

@app.route('/api/list/', methods=['GET'])
@app.route('/api/list/<path:dir_path>', methods=['GET'])
def get_directory_info(dir_path='/'): 
    ''' Return the listing of a supplied path.
    :param dir_path: The directory path to list.
    :type dir_path: String
    :returns: Dictionary containing the directory listing if possible.
    **Example successful JSON return**
        {
            'listing': [
                '/bar/',
                '/baz.txt',
                '/test.txt'
            ]
        }
    **Example failure JSON return**
        {'listing': []}
    '''
    dir_info = []
    clean_list =[]

    try:
        clean_path = _get_clean_directory_path(ARCHIVE_PATH_LEADER, dir_path)
        dir_listing = os.listdir(clean_path)
    except:
        # ValueError - dir_path couldn't be 'cleaned'
        # OSError - clean_path is not a directory
        # Either way, we don't have anything to list for the directory!
        pass
    else:
        # Get product names (there are 2 files .par and .tim)- get only one
        remove_copy_list = [elem for elem in dir_listing if '.par' in elem]
        dir_info = [{'name': elem.split("_",1)[0]
            , 'id': elem.split(".",1)[0]
            , 'dataset': dir_path } for elem in remove_copy_list] 
    
    #if request.query.callback:
    #    return "%s(%s)" % (request.query.callback, {'listing': dir_info})
    return jsonify({'listing': dir_info})




#Helper functions

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)

def get_mimetype(path):
    mimetypes = {
        ".css":  "text/css",
        ".html": "text/html",
        ".js":   "application/javascript",
        ".png":  "image/png",
        ".pdf":  "application/pdf",
        ".txt":  "text/plain",
        ".json":  "application/json"
    }
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    return mimetype


def _get_clean_directory_path(path_leader, dir_path):
    ''' Return a cleaned directory path with a defined path prefix.
    'Clean' dir_path to remove any relative path components or duplicate 
    slashes that could cause problems. The final clean path is then the
    path_leader + dir_path.
    :param path_leader: The path prefix that will be prepended to the cleaned
        dir_path.
    :type path_leader: String
    :param dir_path: The path to clean.
    :type path_leader: String
    
    :returns: The cleaned directory path with path_leader prepended.
    '''
    # Strip out any .. or . relative directories and remove duplicate slashes
    dir_path = re.sub('/[\./]*/?', '/', dir_path)
    dir_path = re.sub('//+', '/', dir_path)

    # Prevents the directory path from being a substring of the path leader.
    # os.path.join('/usr/local/ocw', '/usr/local') gives '/usr/local'
    # which could allow access to unacceptable paths. This also means that
    if dir_path[0] == '/': dir_path = dir_path[1:]

    return os.path.join(path_leader, dir_path)


if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0', port=9880)
