var SERVER_URL = "http://localhost:8000/";
var HEATMAP_SEARCH_URL = "heatmap/search/";
var CALLBACK_URL = "&callback=?";

// notice that all distance (lat, lon, rad) are in degress
// this function considers (year+month+date+hour+minute) of the ts object, if not undefined
// example usages: 
// 		applyLocationData(function(data) {
//						  	call your original function, which takes data as an argument;
//						  },
//						  undefined, undefined, undefined,   // these are the location query params
//						  js_date_object 					 // this is the timestamp query param
//		);
// Warning: Notice that the "timestamp" in the string output is not wrapped with quotation marks
// i.e. 2013-03-14 15:00:00 instead of "2013-03-14 15:00:00"
var applyLocationData = function(callback_func, lat, lon, rad, ts) {
	var coord_url = "";
	var rad_url = "";
	if ((typeof lat !== 'undefined') && (typeof lon !== 'undefined') && (typeof rad !== 'undefined')) {
		coord_url = "coord/"+lat+"/"+lon+"/";
		rad_url = "rad/"+rad+"/";
	}
	var ts_url = "";
	if (typeof ts !== 'undefined') {
		ts_url = "ts/"+ts.getYear()+"/"+ts.getMonth()+"/"+ts.getDate()+"/"+ts.getHours()+"/"+ts.getMinutes()+"/";
	}
	$.getJSON(SERVER_URL+HEATMAP_SEARCH_URL+coord_url+rad_url+ts_url+CALLBACK_URL,
		function(response) {
			// returns a string representation of the JSON object
			var response_str = "{";
			$.each(response, function(timestamp, locations) {
    			response_str += timestamp;
    			response_str += " : [";
    			
    			$.each(locations, function(index) {
    				response_str += "[";
    				response_str += this;
    				response_str += "],"
    			});
	  			// this trims the last ',' character
    			response_str = response_str.substring(0, response_str.length - 1);
    			response_str += "],";
  			});
  			// this trims the last ',' character
  			response_str = response_str.substring(0, response_str.length - 1);
			response_str += "}";

			if ((typeof callback_func !== 'undefined') && (jQuery.isFunction(callback_func))) {
				callback_func(response_str);
			}
	    }
    );
}