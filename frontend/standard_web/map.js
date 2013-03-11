function createNokiaMap(divID, heatmap_data, map_type) {

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
    center: [37.442,  -122.14],
  });

  map.set("baseMapType", nokia.maps.map.Display.SATELLITE);

  var heatmapProvider;
  try {
    // Creating Heatmap overlay
    heatmapProvider = new nokia.maps.heatmap.Overlay({
      // This is the greatest zoom level for which the overlay will provide tiles
      max: 20,
      // This is the overall opacity applied to this overlay
      opacity: 0.6,
      // Defines if our heatmap is value or density based
      type: map_type,
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
    /* We load a data file containing data points for the heat map
     * LoadScript is an helper function and not part of the Nokia Maps API
     * See exampleHelpers.js for implementation details 
     */
     data = heatmap_data;
      // Rendering the heat map overlay onto the map
      heatmapProvider.addData(data);
      map.overlays.add(heatmapProvider);
  }
}
