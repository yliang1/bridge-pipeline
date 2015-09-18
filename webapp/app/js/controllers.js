var bridgeControllers = angular.module('bridgeControllers', []);

var api_url = 'http://thebridge.phys.wvu.edu/api';
var api_url = 'http://127.0.0.1:5000/api';

bridgeControllers.controller('testCont', ['$scope', '$http', function($scope, $http) {
	$scope.os_pdf = '92408/optimal_stat/hd.pdf';
	$scope.api_url = api_url;

}]);


bridgeControllers.controller('ModalInstanceCtrl', ['$scope', '$modalInstance', 'data', 'api_url',
 function($scope, $modalInstance, data, api_url) {
	$scope.modal_data = data;
	$scope.api_url = api_url;

	$scope.cancel = function(){
		$modalInstance.dismiss('cancel');
	}

}]);


bridgeControllers.controller('AnalysisController', ['$scope', '$http','$location', '$anchorScroll', '$modal', '$log',
 function($scope, $http, $location, $anchorScroll,$modal, $log) {

  $scope.animationsEnabled = true;

  $scope.open = function (pulsar) {

    var modalInstance = $modal.open({
      animation: $scope.animationsEnabled,
      templateUrl: 'myModalContent.html',
      controller: 'ModalInstanceCtrl',
      size: 'lg',
      resolve: {
        data: function () {
          return pulsar;
        },
        api_url: function () {
        	return api_url
        }
      }
    });

    modalInstance.result.then(function (selectedItem) {
      $scope.selected = selectedItem;
    }, function () {
      $log.info('Modal dismissed at: ' + new Date());
    });
  };



	$scope.api_url = api_url;
	// Initialize data with default values
	$scope.allSelected 	= {"nanograv5": true,"nanograv9": false, "pptadr1": false};
	$scope.selectText 	= {"nanograv5": "Deselect All","nanograv9": "Select All", "ppta": "Select All"};
	$scope.formData 	= {"timeFilter":"fullTime", "frequencyFilter":"fullFrequency", "residualPlotting":true, "pulsarTiming":false};
	$scope.loading				  = true;
	$scope.hide_plots		 	  = true;
	$scope.hide_analysis 		  = true;
	$scope.hide_analysis_results  = true;
	$scope.hide_engage_analysis   = true;
	$scope.analysis 		      = 'OS';
	$scope.hide_analysis_section = true;
	$scope.hide_loading_analysis = true;
	$scope.hide_analysis_results = true;
	$scope.hide_pulsar_section = false;


	// GET nanograv5 dataset and set as default
	$http.get(api_url+'/list/nanograv5').success(function(data) {
		$scope.nanograv5 = data['listing'];
		// Defualt dataset that has been all checked
		angular.forEach($scope.nanograv5, function(product){
			product.checked = $scope.allSelected["nanograv5"];
		});
	});

	// GET nanograv9 dataset
	$http.get(api_url+'/list/nanograv9').success(function(data) {
		$scope.nanograv9 = data['listing'];
	});


	/* Function that takes in dataset and datasetName in order to 
	 * toggle which products are *all* selected or deselected in the 
	 * dataset selection. 
	*/
	$scope.toggleSeleted = function(dataset,datasetName) {
	    $scope.allSelected[datasetName] = !$scope.allSelected[datasetName];
			angular.forEach(dataset, function(product){
	     	product.checked = $scope.allSelected[datasetName];
			});
	        
	    /*Change the text*/
	    if($scope.allSelected[datasetName]){
	        $scope.selectText[datasetName] = "Deselect All";
	    } else {
	        $scope.selectText[datasetName] = "Select All";
	    }
	};

  /* Function to gather user inputs and process the analysis
   * request by user. Once the "Engage" button is selected, 
   * call http service to python script to run OODT 
   * residual plotting workflow.
  */
  $scope.processAnalysisForm = function() {
  	$scope.loading = false;
  	$scope.disable_engage = true;
  	var selectedData5 = $scope.nanograv5.filter(function(data) {
      return data.checked;
    });
		var selectedData9 = $scope.nanograv9.filter(function(data) {
      return data.checked;
    });

		// Check what dataset the user selected
    if (!jQuery.isEmptyObject(selectedData5)) {
    	$scope.formData['nanograv5'] =jQuery.map( selectedData5, function( p ) {
			  return p.name;
			});
			$scope.formData['dataset'] = 'nanograv5';
    } else if (!jQuery.isEmptyObject(selectedData9)) {
	  	$scope.formData['nanograv9'] =jQuery.map( selectedData9, function( p ) {
			  return p.name;
			});
			$scope.formData['dataset'] = 'nanograv9';
	  }

		// Check that user has selected at least one pulsar
		if (jQuery.isEmptyObject($scope.formData['nanograv5']) 
			&& jQuery.isEmptyObject($scope.formData['nanograv9']) ) {
			alert( 'Please select at least one product to engage!');
		} else {
		
			// If all information is submitted correctly, stringify information to send to API
			var analysisForm = JSON.stringify($scope.formData);

			// Call engage from API
			$http.get(api_url+'/engage/'+analysisForm).success(function(data) {
				$scope.sessionID = data;
				$scope.aData = {}
				$scope.aData['session_id'] = $scope.sessionID.replace(/\s/g, '');
				$scope.aData['analysis'] = 'OS';	
				// If all information is submitted correctly, stringify information to send to API
				var analysisData = JSON.stringify($scope.aData);

				// Call engage from API
				$http.get(api_url+'/analysis/'+analysisData).success(function(data) {
					$scope.sessionID = data;
				});
				// Set timeout for processing plots
				setTimeout(function(){
					// Once session id is returned, gather plots to display
					$http.get(api_url+'/get/plots/'+$scope.sessionID).success(function(data) {
						$scope.plots = data['plot_data'];
						$scope.hide_plots = false;
						$scope.hide_analysis  = false;
						$scope.loading				= true;
					  $scope.disable_engage = false;
					  $scope.hide_engage    = true;
					  $scope.hide_engage_analysis = false;
					});
				}, 5000);
			});
		}
	};
 

  /* Function to gather user inputs and process Bridge analysis. Once 
   * the "Engage" button is selected, call http service to python 
   * script to run OODT workflow for selected analysis.
   */
  $scope.processAnalysis = function() {
  	var selectedData5 = $scope.nanograv5.filter(function(data) {
      return data.checked;
    });
		var selectedData9 = $scope.nanograv9.filter(function(data) {
      return data.checked;
    });

		// Check what dataset the user selected
    if (!jQuery.isEmptyObject(selectedData5)) {
    	$scope.formData['nanograv5'] =jQuery.map( selectedData5, function( p ) {
			  return p.name;
			});
			$scope.formData['dataset'] = 'nanograv5';
    } else if (!jQuery.isEmptyObject(selectedData9)) {
	  	$scope.formData['nanograv9'] =jQuery.map( selectedData9, function( p ) {
			  return p.name;
			});
			$scope.formData['dataset'] = 'nanograv9';
	 	}

   	// Check that user has selected at least one pulsar
		if (jQuery.isEmptyObject($scope.formData['nanograv5']) 
			&& jQuery.isEmptyObject($scope.formData['nanograv9']) ) {
			alert( 'Please select at least one product to engage!');
		} else {
//			$location.hash('analysisResults');
//			// call $anchorScroll()
//			$anchorScroll();

			// show loading and analysis section
			$scope.hide_analysis_section = false;
			$scope.hide_loading_analysis = false;
			// If all information is submitted correctly, stringify information to send to API
			$scope.aData = {}
			$scope.aData['session_id'] = $scope.sessionID;

			analysis = $scope.analysis;
			$scope.aData['analysis'] = analysis;	
			var analysisData = JSON.stringify($scope.aData);
			if (analysis == 'OS') {
				// Call engage from API
				$http.get(api_url+'/analysis/'+analysisData).success(function(data) {
					$scope.sessionID = data;	
					// Set timeout for processing plots
					setTimeout(function(){
						$http.get(api_url+'/get/analysis_data/'+analysisData).success(function(data) {
							$scope.hide_loading_analysis = true;
							$scope.hide_analysis_results = false;
							$scope.analysis_data = data['analysis_data'];
							$scope.disable_analysis_engage = false;
						});
					}, 80000);
				});
			} else if (analysis == 'Fstat') {
				// Call engage from API
				$http.get(api_url+'/analysis/'+analysisData).success(function(data) {
					$scope.sessionID = data;

					// Set timeout for processing plots
					setTimeout(function(){
						$http.get(api_url+'/get/analysis_data/'+analysisData).success(function(data) {
							$scope.hide_loading_analysis = true;
							$scope.hide_analysis_results = false;
							$scope.analysis_data = data['analysis_data'];
							$scope.disable_analysis_engage = false;
						});
					}, 8000);
				});
			}
		}
  };
}]);


bridgeControllers.controller('AboutController', ['$scope', '$http',
 function($scope, $http) {  }]);

