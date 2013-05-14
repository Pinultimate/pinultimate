function TrendMap(div_ID, slider_ID, center_object, zoom_level) 
{
  var me = this;
  this.div_ID = div_ID;

  this.fetched_data = null;
  this.current_data = null;

  this.hour_offset = 0;
  this.reso = 0;

  this.fetched_data_lat_left = null;
  this.fetched_data_lat_right = null;
  this.fetched_data_long_top = null;
  this.fetched_data_long_bottom = null;

  this.RESOLUTION_DIVISIONS = 25;
  this.SERVER_URL = "http://api.pinultimate.net/";
  this.HEATMAP_SEARCH_URL = "heatmap/"
  this.CALLBACK_URL = "&callback=?";

  var createNokiaMap = function(div_ID, center_object, zoom_level)
  {
    nokia.Settings.set( "appId", "ZK2z_y4VG6AbOWUzjvN2");
    nokia.Settings.set( "authenticationToken", "n7NUDiZ7BXw8Hw0YF1ajWQ");

    // Get the DOM node to which we will append the map
    var mapContainer = document.getElementById(div_ID);

    // Create a map inside the map container DOM node
    var map = new nokia.maps.map.Display(mapContainer, {
      components: [
        // Add the behavior component to allow panning / zooming of the map
        new nokia.maps.map.component.Behavior(),
        new nokia.maps.map.component.ZoomBar(),
        new nokia.maps.map.component.Overview(),
        new nokia.maps.map.component.DistanceMeasurement(),
        new nokia.maps.map.component.ScaleBar(),
        new nokia.maps.map.component.TypeSelector()
      ],
      zoomLevel: zoom_level,
      center: center_object, 
        });

    map.set("baseMapType", nokia.maps.map.Display.NORMAL);
    addListenersAndObservers(map);

    return map;
  };

  var addListenersAndObservers = function(map) 
  {
    var dragendHandler = function (evt) {
      me.potentialDataUpdate(false);
    };   

    var listeners = {
      "dragend": [dragendHandler, false, null]
    };

    // Create a default observer for display properties that will just log a message.
    var dragObserver = function (obj, key, newValue, oldValue) {

    };

    var zoomObserver = function (obj, key, newValue, oldValue) {
      //set new radius
      global_zoom_level = newValue;
      global_height = map.getViewBounds().getHeight();
      global_width = map.getViewBounds().getWidth();
      if (newValue < oldValue) {
        me.potentialDataUpdate(false);
      } else {
        me.potentialDataUpdate(true);
      }
    };

    // Template of all map properties we would like to observe
    var observers = {
      "center": dragObserver,
      "zoomLevel": zoomObserver,
    };

    // Add listeners
    map.addListeners(listeners);
    // Add observers
    for (var mapProperty in observers)
      map.addObserver(mapProperty, observers[mapProperty]);
  };

  this.map = createNokiaMap(div_ID, center_object, zoom_level);
  this.potentialDataUpdate(false);
  this.slider = createTimeSlider("sliderContainer", function(new_value) {
    me.hour_offset = 23-new_value;
    console.log("Slider Moved. New Value: " + new_value);
    me.updateCurrentData();
  } ,null);
};

TrendMap.prototype.potentialDataUpdate = function(force) 
{
  var map = this.map;
  console.log("Checking if new data needs to be grabbed...")
  data_bounds_width = map.getViewBounds().getWidth()*2;
  console.log("Data bounds width: " + data_bounds_width.toString());
  data_bounds_height = map.getViewBounds().getHeight()*2;
  resolution = map.getViewBounds().getWidth()/this.RESOLUTION_DIVISIONS;
  this.reso = resolution;
  map_lat_left = map.center.latitude - map.getViewBounds().getWidth()/2;
  map_lat_right = map.center.latitude + map.getViewBounds().getWidth()/2;
  map_long_bottom = map.center.longitude - map.getViewBounds().getHeight()/2;
  map_long_top = map.center.longitude + map.getViewBounds().getHeight()/2;
  if (force || this.firstFetch() || this.newAreaNotCached(map_lat_left,map_lat_right,map_long_top,map_long_bottom)) 
  {
    this.getGridLocationData(this.updateData,map.center.latitude,map.center.longitude,data_bounds_width,data_bounds_height,resolution);
    console.log("New data must be grabbed")
    this.fetched_data_lat_left = map.center.latitude - data_bounds_width/2;
    this.fetched_data_lat_right = map.center.latitude + data_bounds_width/2;
    this.fetched_data_long_bottom = map.center.longitude - data_bounds_height/2;
    this.fetched_data_long_top = map.center.longitude + data_bounds_height/2;
  }
};

TrendMap.prototype.addMarker = function(text,lat,long, radius) 
{
  var iconSVG = 
  '<svg width="__WIDTH__" height="__WIDTH__" xmlns="http://www.w3.org/2000/svg">' +
  '<circle stroke="__ACCENTCOLOR__" fill="__MAINCOLOR__" cx="__RADIUS__" cy="__RADIUS__" r="__RADIUS__" />' +
  '<text x="__RADIUS__" y="__TEXTHEIGHT__" font-size="__FONT__pt" font-family="arial" font-weight="bold" text-anchor="middle" fill="__ACCENTCOLOR__" textContent="__TEXTCONTENT__">__TEXT__</text>' +
   '</svg>';

  circle_radius = 16;
  if (radius != 0) {
    circle_radius *= radius / this.reso;
  }

  svgParser = new nokia.maps.gfx.SvgParser();
  // Helper function that allows us to easily set the text and color of our SVG marker.
  createIcon = function (text, mainColor, accentColor) {
    var svg = iconSVG
      .replace(/__TEXTCONTENT__/g, text)
      .replace(/__TEXT__/g, text)
      .replace(/__ACCENTCOLOR__/g, accentColor)
      .replace(/__RADIUS__/g, circle_radius) 
      .replace(/__TEXTHEIGHT__/g, circle_radius*1.35) 
      .replace(/__FONT__/g, circle_radius*0.625) 
      .replace(/__WIDTH__/g, circle_radius*2)      
      .replace(/__MAINCOLOR__/g, mainColor);
    return new nokia.maps.gfx.GraphicsImage(svgParser.parseSvg(svg));
  };
  var markerIcon = createIcon(text, "#43A51B", "#FFF");
  var marker = new nokia.maps.map.Marker([lat, long], {icon: markerIcon});
  this.map.objects.add(marker);
};

TrendMap.prototype.removeAllMarkers = function() 
{
  this.map.objects.clear();
};

TrendMap.prototype.firstFetch = function()
{
  if (this.fetched_data_lat_left === null || this.fetched_data_lat_right === null || this.fetched_data_long_top === null || this.fetched_data_long_bottom === null) 
  {
    console.log("First fetch");
    return true;
  } else 
  {
    return false;
  }
};

TrendMap.prototype.newAreaNotCached = function(new_lat_left,new_lat_right,new_long_top,new_long_bottom) 
{
  /*
  console.log("New Lat Left: " + new_lat_left.toString());
  console.log("Old Lat Left: " + fetched_data_lat_left.toString());
  console.log("New Lat Right: " + new_lat_right.toString());
  console.log("Old Lat Right: " + fetched_data_lat_right.toString());
  console.log("New Long Top: " + new_long_top.toString());
  console.log("Old Long Top: " + fetched_data_long_top.toString());
  console.log("New Long Bot: " + new_long_bottom.toString());
  console.log("Old Long Bot: " + fetched_data_long_bottom.toString());
  */
  if (new_lat_left < this.fetched_data_lat_left || new_lat_right > this.fetched_data_lat_right || new_long_bottom < this.fetched_data_long_bottom || new_long_top > this.fetched_data_long_top) 
  {
    console.log("Area not cached");
    return true;
  } else 
  {
    return false;
  }
};

TrendMap.prototype.makeMarkers = function(clustered_data)
{
  for (var i=0; i < clustered_data.length; i++) 
  {
    this.addMarker(clustered_data[i].count.toString(),clustered_data[i].latitude,clustered_data[i].longitude,clustered_data[i].radius);
  }
};

TrendMap.prototype.updateData = function(json_object) 
{
  var me = this;
  var parseHourFromTimeStamp = function(timestamp_string)
  {
    var index_of_space = timestamp_string.indexOf(" ");
    var index_of_colon = timestamp_string.indexOf(":");
    //console.log("Index of Space: " + index_of_space);
    //console.log("Index of Colon: " + index_of_colon);
    hour_string = timestamp_string.substring(index_of_space+1,index_of_colon);
    //console.log("Hour String: " + hour_string);
    // parseInt doesn't play nicely if the string is has a zero as the first character
    if (hour_string[0] === "0") {
      hour_string = hour_string[1];
    }
    return parseInt(hour_string);
  }

  // Takes JSON response and creates an array of objects for TrendMap to work with
  var translateResponse = function(json_object)
  {
    var array_of_time_data = json_object.response;
    var translated_data = new Array();
    for (var i=0; i < 24; i++) {
      translated_data.push({"locations":[]});
    }
    var current_hour = new Date().getHours();
    var data_index = array_of_time_data.length-1;
    for (var i=23; i >= 0; i--) {
      data_hour = parseHourFromTimeStamp(array_of_time_data[data_index].timestamp);
      console.log("Current Hour: "+ current_hour);
      console.log("Data Hour: " + data_hour)
      if (data_hour === current_hour){
        translated_data[i] = array_of_time_data[data_index];
        data_index--;
      }
      current_hour--;
      if (current_hour < 0) {
        current_hour = 23;
      }
    }
    return translated_data
  }
  
  this.fetched_data = translateResponse(json_object);
  if (this.fetched_data.length-1-this.hour_offset >= 0) 
  {
    this.updateCurrentData();
  } else {
    console.log("Hour offset went negative!");
  }
};

TrendMap.prototype.updateCurrentData = function()
{
  console.log(this.fetched_data);
  this.current_data = this.fetched_data[this.fetched_data.length-1-this.hour_offset];
  //console.log(this.current_data);
  var clustered_data = ClusteringProcessor(this.current_data.locations);
  this.removeAllMarkers();
  this.makeMarkers(clustered_data);
}

TrendMap.prototype.getGridLocationData = function(callback_func, lat_center, long_center, lat_range, long_range, resolution) {
  var me = this;
  var data_url = this.SERVER_URL + this.HEATMAP_SEARCH_URL;
  data_url += "resolution/" + resolution + "/";
  data_url += "search/center/" + lat_center + "/" + long_center + "/";
  data_url += "region/" + lat_range + "/" + long_range + "/";

  var date = new Date();
  
  var today_year = date.getFullYear();
  var today_month = date.getMonth()+1;
  var today_day = date.getDate();
  var today_hour = date.getHours();

  var today_milliseconds = Date.UTC(today_year,today_month,today_day,today_hour);
  var yesterday_milliseconds = today_milliseconds - (24*3600*1000); // 24 hours * 60 minutes * 60 seconds * 1000 milliseconds

  console.log("Today: " + today_year.toString() + "/" + today_month.toString() + "/" + today_day.toString() + " " + today_hour.toString());

  var yesterday_date = new Date(yesterday_milliseconds);
  var yesterday_year = yesterday_date.getFullYear();
  var yesterday_month = yesterday_date.getMonth();
  var yesterday_day = yesterday_date.getDate();
  var yesterday_hour = date.getHours();

  data_url += "from/" + yesterday_year + "/" + yesterday_month + "/" + yesterday_day + "/" + yesterday_hour +"/";

  data_url += "to/"+ today_year + "/" + today_month + "/" + today_day + "/" + today_hour + "/";

  console.log("24 hours ago: " + yesterday_year.toString() + "/" + yesterday_month.toString() + "/" + yesterday_day.toString() + " " + yesterday_hour.toString());

  data_url += this.CALLBACK_URL; // Need CALLBACK_URL For Jsonp

  


  $.getJSON(data_url)
    .done(function(response) {
      $("#loading").hide();
      // Once request is recieved, call the call_back function
      me.updateData(response);
    }).fail(function() {
      $("#loading").hide();
      console.log("Getting grid data failed"); 
    });
  $("#loading").show();
}

TrendMap.prototype.setHourOffset = function(hour_offset)
{
  this.hour_offset = hour_offset;
}