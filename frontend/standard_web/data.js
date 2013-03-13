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
var applyLocationData = function(callback_func, lat, lon, rad, ts, discard_hour, discard_minute) {
	var coord_url = "";
	var rad_url = "";
	if ((typeof lat !== 'undefined') && (typeof lon !== 'undefined') && (typeof rad !== 'undefined')) {
		coord_url = "coord/"+lat+"/"+lon+"/";
		rad_url = "rad/"+rad+"/";
	}

	if (typeof discard_hour === 'undefined') {
		discard_hour = false;
	}
	if (typeof discard_minute === 'undefined') {
		discard_minute = false;
	}
	var ts_url = "";
	if (typeof ts !== 'undefined') {
		ts_url = "ts/"+ts.getYear()+"/"+ts.getMonth()+"/"+ts.getDate()+"/";
		if (!discard_hour) {
			ts_url += ts.getHours()+"/";
			if (!discard_minute) {
				ts_url += ts.getMinutes()+"/";
			}
		}
	}
	$.getJSON(SERVER_URL+HEATMAP_SEARCH_URL+coord_url+rad_url+ts_url+CALLBACK_URL,
		function(response) {
			// returns a string representation of the JSON object
			var response_str = stringifyLocationJSON(response);

			if ((typeof callback_func !== 'undefined') && (jQuery.isFunction(callback_func))) {
				callback_func(response_str);
			}
	    }
    );
}

var applyLocationDataReg = function(callback_func, lat, lon, latrange, lonrange, ts, discard_hour, discard_minute) {
	var coord_url = "";
	var reg_url = "";
	if ((typeof lat !== 'undefined') && (typeof lon !== 'undefined') && (typeof latrange !== 'undefined') && (typeof lonrange !== 'undefined')) {
		coord_url = "coord/"+lat+"/"+lon+"/";
		reg_url = "reg/"+latrange+"/"+lonrange+"/";
	}

	if (typeof discard_hour === 'undefined') {
		discard_hour = false;
	}
	if (typeof discard_minute === 'undefined') {
		discard_minute = false;
	}
	var ts_url = "";
	if (typeof ts !== 'undefined') {
		ts_url = "ts/"+ts.getYear()+"/"+ts.getMonth()+"/"+ts.getDate()+"/";
		if (!discard_hour) {
			ts_url += ts.getHours()+"/";
			if (!discard_minute) {
				ts_url += ts.getMinutes()+"/";
			}
		}
	}
	$.getJSON(SERVER_URL+HEATMAP_SEARCH_URL+coord_url+rad_url+ts_url+CALLBACK_URL,
		function(response) {
			// returns a string representation of the JSON object
			var response_str = stringifyLocationJSON(response);
			if ((typeof callback_func !== 'undefined') && (jQuery.isFunction(callback_func))) {
				callback_func(response_str);
			}
	    }
    );
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