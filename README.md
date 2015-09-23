# bridge-pipeline 
The Bridge pipeline.
===================


----------


The Bridge pipeline uses Apache Object Oriented Data Technology (OODT) for data
processing. Apache OODT integrates and archives your processes, your data, and
its metadata (https://oodt.apache.org/).

#### <i class="icon-folder-open"></i> OODT code structure:
> - **bin** -- Holds env.sh (where all environment variables are located) and oodt script (used to start and stop oodt)   
> - **data**  
> -- **archive** -- Holds all the datasets (format for datasets is name_of_dataset i.e. 'nanograv5' and include all .tim and .par files and nothing else)  
> -- **jobs** -- Holds all the processed information from workflow (format - web app sets a session_id for each run. there will be a directory with that session_id and all the output data will be stored within this directory. All plots generated by residual plotting is in 'plots'. All optimal stat data is stored in 'optimal_stat'. All f stat data is stored in 'f_stat'. and average epoch output is stored in 'avg_epoch'. The dataset used for the session id is stored in 'session_data'. This directory can be clean nightly or weekly to regain some space.  
> -- **workflow** -- Stores a catalog of all workflows run. If you ever want to remove all the workflow data which appears in the OODT opsui, delete the complete directory (not just the contents).   
> - **logs**    ⁃ oodt.out - Holds all the logs for the entire OODT system. When running into issues, this is the first place you should check for possible reasons.   
> - **pge** --    
> -- **bridge**  -- All the functional bridge code from the git repository should be cloned here. (This directory does not exist. Deployer should create it.)   
> -- **bin** -- Holds helpful Python scripts to run workflows    
> -- **policy** -- Holds PGE configuration files. Each workflow has it's own configuration file used to set env vars and commands to run.   
> - workflow   
> -- **etc** -- Set logging properties or workflow properties 
> -- **logs** -- Holds workflow logs
> -- **policy** -- Define workflows here. For an addition of a workflow, you will need to edit the events.xml, tasks.xml and create a new workflow file to define where the pge configuration file is located (so create a pge config (pge/policy) for you workflow as well)


----------


####The User Interface (UI) code uses AngularJS , an open-source (javascript) web application framework.

#### <i class="icon-folder-open"></i> UI code structure:

 > - **app** - Angular web application   ⁃ css -- This directory holds all CSS stylesheets.   
 > -- **img** -- This directory holds all images needed for the UI. 
 > -- **js** -- This directory holds all Javascript files.
 > -- **lib** -- This directory holds all libraries used. i.e. Bootstrap, Angular
 > -- **partials** -- This directory holds different views (pages)


**Partials directory**: In this directory you can find 2 main HTML files. The
about.html file is the home page of the web app. This is where the introduction
and instructions for the application are given. In the analysis.html file, you
will find all the HTML and angular data-binding for the main application.

> For example, you can see that the data selection "accordion", advanced options, the engage buttons, and the result views are all defined within this page.
> 
> Comments in HTML are enclosed in `<!-- comment -->` (and it appears in blue in vi)

**js directory**: In this directory you will find all the JS code that controls the
HTML. In this application we use an angular route library (found in lib/angualr
dir) to route the appropriate pages when navigation buttons are selected. All
the control is defined in the app.js file.

All the control for the about.html and analysis.html page is defined in the
controller.js file. The controller specifically for the analysis.html page is
called 'AnalysisController'. On line 3, you should set the proper 'api_url' that
point to your flask API. within the 'AnalysisController', you will see that on
line 30 (at the time of documentation) all the defaults for the analysis view is
set.
