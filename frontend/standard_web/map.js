function createNokiaMap(div_ID, center_object, zoom_level)
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

  map.set("baseMapType", nokia.maps.map.Display.SATELLITE);
  addListenersAndObservers(map);

  return map;
}

function addListenersAndObservers(map) {
  var dragendHandler = function (evt) {
    var center_geo = map.getViewBounds().getCenter();
    console.log(center_geo.latitude);
    console.log(center_geo.longitude);
    //applyLocationData(updateData,global_lat,global_long,global_zoom_level,global_ts);
    //applyLocationData(updateData);
  };   

  var listeners = {
    "dragend": [dragendHandler, false, null]
  };

  // Create a default observer for display properties that will just log a message.
  var dragObserver = function (obj, key, newValue, oldValue) {

      console.log(newValue.longitude);
      console.log(newValue.latitude);
  };

  var zoomObserver = function (obj, key, newValue, oldValue) {
    //set new radius
    global_zoom_level = newValue;
    global_height = map.getViewBounds().getHeight();
    global_width = map.getViewBounds().getWidth();
    console.log(global_height);
    console.log(global_width);
    if (newValue > oldValue) {
      //applyLocationData(updateData,global_lat,global_long,global_zoom_level,global_ts);
      //applyLocationData(updateData);
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

function addMarker(map,text,lat,long, radius) {
  var iconSVG = 
  '<svg width="32" height="32" xmlns="http://www.w3.org/2000/svg">' +
  '<circle stroke="__ACCENTCOLOR__" fill="__MAINCOLOR__" cx="16" cy="16" r="16" />' +
  '<text x="16" y="20" font-size="10pt" font-family="arial" font-weight="bold" text-anchor="middle" fill="__ACCENTCOLOR__" textContent="__TEXTCONTENT__">__TEXT__</text>' +
  '</svg>',
  svgParser = new nokia.maps.gfx.SvgParser(),
  // Helper function that allows us to easily set the text and color of our SVG marker.
  createIcon = function (text, mainColor, accentColor) {
    var svg = iconSVG
      .replace(/__TEXTCONTENT__/g, text)
      .replace(/__TEXT__/g, text)
      .replace(/__ACCENTCOLOR__/g, accentColor)
      .replace(/__RADIUS__/g, radius)
      .replace(/__MAINCOLOR__/g, mainColor);
    return new nokia.maps.gfx.GraphicsImage(svgParser.parseSvg(svg));
  };
  var markerIcon = createIcon(text, "#43A51B", "#FFF");
  var marker = new nokia.maps.map.Marker(
    // Center GeoCoordinates
    [lat, long], 
    {
      icon: markerIcon
    }
  );
  map.objects.add(marker);
};



/* Heatmap stuff */

function createNokiaHeatMap(divID, heatmap_data, map_type, centerObejct) {

  nokia.Settings.set( "appId", "ZK2z_y4VG6AbOWUzjvN2");
  nokia.Settings.set( "authenticationToken", "n7NUDiZ7BXw8Hw0YF1ajWQ");

  // Get the DOM node to which we will append the map
  var mapContainer = document.getElementById(divID);

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
    zoomLevel: 13,
    center: centerObejct, 
      });

  map.set("baseMapType", nokia.maps.map.Display.SATELLITE);
  var heatMapOverlay = createHeatMapOverlay(heatmap_data,map_type);
  map.overlays.add(heatMapOverlay);

  return map;
}

function createHeatMapOverlay(heatMapData,heatMapType) {
  var heatmapProvider;
  try {
    // Creating Heatmap overlay
    heatmapProvider = new nokia.maps.heatmap.Overlay({
      // This is the greatest zoom level for which the overlay will provide tiles
      max: 20,
      // This is the overall opacity applied to this overlay
      opacity: 0.6,
      // Defines if our heatmap is value or density based
      type: heatMapType,
      // Coarseness defines the resolution with which the heat map is created.
      coarseness: 2
    });
  } catch (e) {
    // The heat map overlay constructor throws an exception if there
    // is no canvas support in the browser
    alert(typeof e == "string" ? e : e.message);
  }
  // Only start loading data if the heat map overlay was successfully created
  if (heatmapProvider) {
    // Rendering the heat map overlay onto the map
    heatmapProvider.addData(heatMapData);
  }
  return heatmapProvider;
}
