function TrendMap(div_ID, slider_ID, center_object, zoom_level) 
{
  var me = this;
  this.div_ID = div_ID;

  this.fetched_data = null;
  this.current_data = null;

  this.hour_offset = 1; 
  this.reso = 0;
  this.countMax = 0;
  this.countMin = 0;  
  this.countMean = 0;

  this.DEFAULT_CLUSTER_RADIUS = 16; // in px
  this.MIN_CLUSTER_RADIUS = 8;
  this.MAX_CLUSTER_RADIUS = 24;

  this.fetched_data_lat_left = null;
  this.fetched_data_lat_right = null;
  this.fetched_data_long_top = null;
  this.fetched_data_long_bottom = null;

  this.RESOLUTION_DIVISIONS = 25;
  this.SERVER_URL = "http://api.pinultimate.net/";
  this.HEATMAP_SEARCH_URL = "heatmap/"
  this.CALLBACK_URL = "&callback=?";
  this.ANALYTICS_URL = this.SERVER_URL+ "analytics/";
  this.UPDATE_TIME_INTERVAL = 15000;

  this.MIN_DATA_POINTS_TO_CLUSTER = 0;

  // Interval to call analytics for time
  setInterval(function() {
    var update_user_time_url = me.ANALYTICS_URL + "update/";
    $.post(update_user_time_url).done(function() {
      console.log("User time update success");
    }).fail(function() {
      console.log("User time update failure");
    });
  }, me.UPDATE_TIME_INTERVAL);

  var createNokiaMap = function(div_ID, center_object, zoom_level)
  {
    nokia.Settings.set( "appId", "ZK2z_y4VG6AbOWUzjvN2");
    nokia.Settings.set( "authenticationToken", "n7NUDiZ7BXw8Hw0YF1ajWQ");

    // Get the DOM node to which we will append the map
    var mapContainer = document.getElementById(div_ID);
    me.infoBubbles = new nokia.maps.map.component.InfoBubbles();
    // Create a map inside the map container DOM node
    var map = new nokia.maps.map.Display(mapContainer, {
      components: [
        me.infoBubbles,
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
      if (newValue < oldValue) {
        me.potentialDataUpdate(true);
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
  this.slider = new TimeSlider("sliderContainer", function(new_value) {
    me.hour_offset = 24-new_value;
    console.log("Slider Moved. New Value: " + new_value);
    me.updateCurrentData();
  });
};

TrendMap.prototype.potentialDataUpdate = function(force) 
{
  var map = this.map;
  console.log("Checking if new data needs to be grabbed...")
  data_bounds_width = map.getViewBounds().getWidth()*1.0;
  data_bounds_height = map.getViewBounds().getHeight()*1.0;
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

TrendMap.prototype.addMarker = function(count,lat,long,radius, twitter_count, instagram_count, flickr_count) 
{
  var me = this;
  //Returns an array of colors for the drawing, array[0] is main color, array[1] is shadow color
  var decideColors = function(count,mean_count,level)
  {
    var color = [{"Center": "#FF0000", "Shadow": "#FF3200"},{"Center": "#FF04F0", "Shadow": "#FF07F0"}, {"Center": "#FFD700", "Shadow": "#FFFF00"}, {"Center": "#43A51B", "Shadow": "#43A51B"}, {"Center": "#0054ff", "Shadow": "#0084ff"}];
    var mainColor = color[2].Center;;
    var shadowColor = color[2].Center;
    if (count > mean_count + 2*level) {
      mainColor = color[0].Center;
      shadowColor = color[0].Shadow;
    } else if (count > mean_count + level) {
      mainColor = color[1].Center;
      shadowColor = color[1].Shadow;
    } else if (count < mean_count - level) {
      mainColor = color[3].Center;
      shadowColor = color[3].Shadow;
    } else if (count < mean_count - 2*level) {
      mainColor = color[4].Center;
      shadowColor = color[4].Shadow;
    }
    return [mainColor,shadowColor];
  };

  //Creates and returns a marker icon
  var createIcon = function (text, mainColor, accentColor, secondColor, opacity, circle_radius) 
  {
    var svgParser = new nokia.maps.gfx.SvgParser();
    var iconSVG = 
  '<svg width="__WIDTH__" height="__WIDTH__" xmlns="http://www.w3.org/2000/svg">' +
  '<circle stroke="__SECONDCOLOR__" fill="__SECONDCOLOR__" cx="__DISPLACEMENT2__" cy="__DISPLACEMENT2__" r="__RADIUS2__" opacity="__OPACITY__"/>' +
  '<circle stroke="__MAINCOLOR__" fill="__MAINCOLOR__" cx="__DISPLACEMENT__" cy="__DISPLACEMENT__" r="__RADIUS__" />' +
  '<text x="__DISPLACEMENT__" y="__TEXTHEIGHT__" font-size="__FONT__pt" font-family="arial" font-weight="bold" text-anchor="middle" fill="__ACCENTCOLOR__" textContent="__TEXTCONTENT__">__TEXT__</text>' +
  '</svg>';
    var svg = iconSVG
      .replace(/__OPACITY__/g, opacity)
      .replace(/__TEXTCONTENT__/g, text)
      .replace(/__TEXT__/g, text)
      .replace(/__ACCENTCOLOR__/g, accentColor)
      .replace(/__RADIUS__/g, circle_radius) 
      .replace(/__DISPLACEMENT__/g, circle_radius)
      .replace(/__DISPLACEMENT2__/g, circle_radius)
      .replace(/__TEXTHEIGHT__/g, circle_radius*1.35) 
      .replace(/__FONT__/g, circle_radius*0.625) 
      .replace(/__WIDTH__/g, circle_radius*2)      
      .replace(/__MAINCOLOR__/g, mainColor)
      .replace(/__SECONDCOLOR__/g, secondColor)
      .replace(/__RADIUS2__/g, circle_radius*1.5)
    return new nokia.maps.gfx.GraphicsImage(svgParser.parseSvg(svg));
  };

  var count_text = count.toString();
  
  // Determine radius for cluster
  var cluster_circle_radius = me.DEFAULT_CLUSTER_RADIUS;
  if (radius !== undefined && radius !== 0) {
    cluster_circle_radius *= radius / this.reso;
    if (cluster_circle_radius < me.MIN_CLUSTER_RADIUS) cluster_circle_radius = me.MIN_CLUSTER_RADIUS;
    if (cluster_circle_radius > me.MAX_CLUSTER_RADIUS) cluster_circle_radius = me.MAX_CLUSTER_RADIUS;
  }

  // Create marker icons
  var level = Math.floor((this.countMax - this.countMin) / 5); 
  var colors = decideColors(count,this.countMean,level);
  var mainColor = colors[0];
  var shadowColor = colors[1]; 
  var markerIcon = createIcon(count_text, mainColor, "#FFF", shadowColor, 0, cluster_circle_radius);
  var markerIconOnHover = createIcon(count_text, mainColor, "#FFF", shadowColor, 0.3, cluster_circle_radius);

  var marker = new nokia.maps.map.Marker([lat, long], {icon: markerIcon});


  marker.addListener("mouseover", function (evt) {
    marker.set("icon", markerIconOnHover);
    /* Display's update() can be used to force an immediate re-render of the current view 
     * instead of the default delayed one, we do this to make the icons switch instantly on mouse over.
     */
    //map.update(-1, 0);
  });
  marker.addListener("mouseout", function (evt) {
    marker.set("icon", markerIcon);
    //map.update(-1, 0);
  });

  // Define Touch Listener
  var TOUCH = nokia.maps.dom.Page.browser.touch,
  CLICK = TOUCH ? "tap" : "click";
  marker.addListener(CLICK, function(evt) {
    // Create Info Bubble
    var info_bubble_text = "<div style='background-color:" + mainColor + "'>" + 
    "<p><font size='2'> Counts from </font></p>" +
    "<p>Twitter:" + twitter_count + "</p>" +
    "<p> Instagram: " + instagram_count + "</p>" +
    "<p> Flickr: " + flickr_count + "</p>" +
    "</div>" ;
    // Info bubble requires a coordinate, not just a lat-long
    var boundingbox = marker.getDisplayBoundingBox(me.map);
    var width = boundingbox.bottomRight.x - boundingbox.topLeft.x;
    var height = boundingbox.bottomRight.y - boundingbox.topLeft.y;
    var x = boundingbox.topLeft.x + width/2;;
    var y = boundingbox.topLeft.y + height/2;
    var bubblecoord = me.map.pixelToGeo(x, y);
    me.infoBubbles.openBubble(info_bubble_text,bubblecoord);
    var tap_url = me.ANALYTICS_URL + "tap/";
    $.post(tap_url).done(function() {
      console.log("Tap POST success");
    }).fail(function(request_object,status,error_message) {
      console.log("Tap POST failed");
      console.log("status: " + status);
      console.log("Error Message: " + error_message);
    })
  });


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
    console.log("Area was cached, no request sent");
    return false;
  }
};

TrendMap.prototype.makeMarkers = function(clustered_data)
{  
  this.countMin = 0;
  this.countMax = this.countMin;
  var sum  = 0;
  // Count total number of check-ins to decide weights for colors
  for (var i=1; i < clustered_data.length; i++) 
  { 
    sum += clustered_data[i].count;
    if (clustered_data[i].count > this.countMax) this.countMax = clustered_data[i].count;
    if (clustered_data[i].count < this.countMin) this.countMin = clustered_data[i].count;
  }
  this.countMean = sum / clustered_data.length;

  for (var i=0; i < clustered_data.length; i++) 
  {  
    // Add markers
    this.addMarker(clustered_data[i].count,clustered_data[i].latitude,clustered_data[i].longitude,clustered_data[i].radius,clustered_data[i].twitter,clustered_data[i].instagram,clustered_data[i].flickr);
  }
};

TrendMap.prototype.updateData = function(json_object) 
{
  var me = this;
  var parseHourFromTimeStamp = function(timestamp_string)
  {
    var index_of_space = timestamp_string.indexOf(" ");
    var index_of_colon = timestamp_string.indexOf(":");
    hour_string = timestamp_string.substring(index_of_space+1,index_of_colon);
    // parseInt doesn't play nicely if the string is has a zero as the first character
    if (hour_string[0] === "0") {
      hour_string = hour_string[1];
    }
    return parseInt(hour_string);
  }

  // Takes JSON response and creates an array of objects for TrendMap to work with
  var translateResponse = function(json_object)
  {
    var fetched_time_data = json_object.response;
    var translated_data = new Array();
    for (var i=0; i < 24; i++) {
      translated_data.push({"locations":[]});
    }
    var current_hour = new Date().getHours();
    var data_index = fetched_time_data.length-1;
    for (var i=23; i >= 0; i--) {
      data_hour = parseHourFromTimeStamp(fetched_time_data[data_index].timestamp);
      //console.log("Current Hour: "+ current_hour);
      //console.log("Data Hour: " + data_hour);
      // If data exists for this hour, supply the data
      if (data_hour === current_hour){
        translated_data[i] = fetched_time_data[data_index];
        // Decrement current index counter for fetched_data
        data_index--;
      }
      // Always decrement counter for current hour index
      current_hour--;

      // To yesterday?
      if (current_hour < 0) {
        // Went back to the day before
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
  var data_to_display = this.current_data.locations;
  // Potential Cluster Threshold
  if (data_to_display.length > this.MIN_DATA_POINTS_TO_CLUSTER) {
    // Perform Clustering
    data_to_display = ClusteringProcessor(data_to_display);
  }
  this.removeAllMarkers();
  //console.log(data_to_display);
  this.makeMarkers(data_to_display);
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

  console.log("Today: " + today_year.toString() + "/" + today_month.toString() + "/" + today_day.toString() + " " + today_hour.toString() + ":00");

  var yesterday_date = new Date(yesterday_milliseconds);
  var yesterday_year = yesterday_date.getFullYear();
  var yesterday_month = yesterday_date.getMonth();
  var yesterday_day = yesterday_date.getDate();
  var yesterday_hour = date.getHours();

  data_url += "from/" + yesterday_year + "/" + yesterday_month + "/" + yesterday_day + "/" + yesterday_hour +"/";
  data_url += "to/"+ today_year + "/" + today_month + "/" + today_day + "/" + today_hour + "/";
  console.log("24 hours ago: " + yesterday_year.toString() + "/" + yesterday_month.toString() + "/" + yesterday_day.toString() + " " + yesterday_hour.toString() +":00");

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