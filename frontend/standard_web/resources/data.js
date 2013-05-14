//var SERVER_URL = "http://localhost:8000/";
var SERVER_URL = "http://api.pinultimate.net/";
var HEATMAP_SEARCH_URL = "heatmap/"
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

var getGridLocationData = function(callback_func, lat_center, long_center, lat_range, long_range, resolution) {
  var data_url = SERVER_URL + HEATMAP_SEARCH_URL;
  data_url += "resolution/" + resolution + "/";
  data_url += "search/center/" + lat_center + "/" + long_center + "/";
  data_url += "region/" + lat_range + "/" + long_range + "/";
  data_url += CALLBACK_URL; // Need CALLBACK_URL For Jsonp
  console.log(data_url);
  $.getJSON(data_url)
    .done(function(response) {
      // Once request is recieved, call the call_back function
      callback_func(response);
    }).fail(function() {
      console.log("Getting grid data failed"); 
    });
}

var stringifyLocationJSON = function(response) {
    var response_str = "{";
    $.each(response, function(timestamp, locations) {
            var spaceIndex= timestamp.indexOf(" ");
            var colonIndex = timestamp.indexOf(":");
            var hour = timestamp.substring(spaceIndex+1,colonIndex);
            console.log(hour);
    response_str += '"' + parseInt(hour,10) + '"'; // For now we want hours
    response_str += " : [";

    $.each(locations, function(index) {
            response_str += "{";
            console.log(this);
            response_str += '"latitude":' + this[0] + ",";
            response_str += '"longitude":' + this[1];
            response_str += "},"
    });
            // this trims the last ',' character
    response_str = response_str.substring(0, response_str.length - 1);
    response_str += "],";
    });
    // this trims the last ',' character
    response_str = response_str.substring(0, response_str.length - 1);
    response_str += "}";
    return response_str;
}