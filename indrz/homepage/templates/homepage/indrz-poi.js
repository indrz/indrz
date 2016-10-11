
$("#showPoi").submit(function (event) {
      alert( "Handler for .submit() called." + $('#poi-input').val()   );
    // var startNum = $('#route-from').val();
    // var endNum = $('#route-to').val();
    // var rType = $("input:radio[name=typeRoute]:checked").val();
    // addRoute(startNum, endNum, rType);
    event.preventDefault();
});

var poiLayer;

function searchPoi(campusId, searchString) {
    // var searchUrl = '/api/v1/buildings/' + buildingId + '/' + spaceName + '.json';
    // var searchUrl = baseApiUrl + 'campus/' + campusId + '/search/' + searchString + '?format=json';
    var searchUrl = baseApiUrl + "campus/1/poi/name/" + searchString + '/?format=json';
    console.log("in searchPOI: " + searchUrl);

    if (poiLayer) {
        map.removeLayer(poiLayer);
        console.log("removing poi layer now");
        //map.getLayers().pop();
    }


    var searchSource = new ol.source.Vector();
    $.ajax(searchUrl).then(function (response) {
        console.log("in response: " + response);
        var geojsonFormat3 = new ol.format.GeoJSON();
        var featuresSearch = geojsonFormat3.readFeatures(response,
            {featureProjection: 'EPSG:4326'});
        searchSource.addFeatures(featuresSearch);

        // zoomToFeature(searchSource);


        var centerCoord = ol.extent.getCenter(searchSource.getExtent());
        console.log(centerCoord);

        open_popup(featuresSearch[0].getProperties(), centerCoord);

        var poi_id = response.features[0].id;

        // active the floor of the start point
        var searchResFloorNum = featuresSearch[0].getProperties().floor_num;
        for (var i = 0; i < switchableLayers.length; i++) {
            if (searchResFloorNum == switchableLayers[i].getProperties().floor_num) {
                activateLayer(i);
            }
        }

    });



    var iconFeature = new ol.Feature({
        geometry: new ol.geom.Point([0, 0]),
        name: 'Null Island',
        population: 4000,
        rainfall: 500
      });

    var iconStyle = new ol.style.Style({
            image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
              anchor: [0.5, 46],
              anchorXUnits: 'fraction',
              anchorYUnits: 'pixels',
              src: '/static/access_other_stairs.png'
            }))
          });

      iconFeature.setStyle(iconStyle);

      var vectorSource = new ol.source.Vector({
        features: [iconFeature]
      });

      var vectorLayer = new ol.layer.Vector({
        source: vectorSource
      });



    poiLayer = new ol.layer.Vector({
        source: searchSource,
        style: iconStyle,
        title: "poiLayer",
        name: "poiLayer",
        zIndex: 999
    });

    map.getLayers().push(poiLayer);
    // $("#clearSearch").removeClass("hide");
    // $("#shareSearch").removeClass("hide");

}



  //
  // var element = document.getElementById('popup');
  //
  // var popup = new ol.Overlay({
  //   element: element,
  //   positioning: 'bottom-center',
  //   stopEvent: false,
  //   offset: [0, -50]
  // });
  // map.addOverlay(popup);
  //
  // // display popup on click
  // map.on('click', function(evt) {
  //   var feature = map.forEachFeatureAtPixel(evt.pixel,
  //       function(feature) {
  //         return feature;
  //       });
  //   if (feature) {
  //     var coordinates = feature.getGeometry().getCoordinates();
  //     popup.setPosition(coordinates);
  //     $(element).popover({
  //       'placement': 'top',
  //       'html': true,
  //       'content': feature.get('name')
  //     });
  //     $(element).popover('show');
  //   } else {
  //     $(element).popover('destroy');
  //   }
  // });
  //
  // // change mouse cursor when over marker
  // map.on('pointermove', function(e) {
  //   if (e.dragging) {
  //     $(element).popover('destroy');
  //     return;
  //   }
  //   var pixel = map.getEventPixel(e.originalEvent);
  //   var hit = map.hasFeatureAtPixel(pixel);
  //   map.getTarget().style.cursor = hit ? 'pointer' : '';
  // });