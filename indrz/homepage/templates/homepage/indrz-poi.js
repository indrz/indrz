// var poiLayer;
var poiLayerName;

var poiLayers = [];


function testCreatePoi(layername) {

    var poiUrl = baseApiUrl + "campus/1/poi/name/" + layername + '/?format=json';

    var source = new ol.source.Vector();

    fetch(poiUrl).then(function (response) {
        return response.json();
    }).then(function (json) {
        var format = new ol.format.GeoJSON();
        var features = format.readFeatures(json, {featureProjection: 'EPSG:3857'});

        source.addFeatures(features);
    });

    var vectorLayer = new ol.layer.Vector({
        source: source,
        title: layername
    });
    console.log("now pushin new poi layer to group")
    poiLayerGroup.getLayers().push(vectorLayer)

    return vectorLayer;
}

// testCreatePoi("Entrance")
// testCreatePoi("Info Point")

function listPoiProperties() {

    map.getLayers().forEach(function (layer, i) {

        // bindInputs('#layer' + i, layer);
        if (layer instanceof ol.layer.Group) {
            console.log("Group Name is : " + layer.getProperties().name)
            layer.getLayers().forEach(function (sublayer, j) {
                console.log("Layer name: " + sublayer.getProperties().name)
                //bindInputs('#layer' + i + j, sublayer);

            });
        }
    });

}


function listAllLayers() {

    map.getLayers().forEach(function (layer, i) {

        // bindInputs('#layer' + i, layer);
        if (layer instanceof ol.layer.Group) {
            // console.log("Group Name is : " + layer.getProperties().name)
            layer.getLayers().forEach(function (sublayer) {

                // map.removeLayer(layer);


                    console.log("layer name : " + sublayer.getProperties().name)
                    console.log("layer visibility : " + sublayer.getVisible())




            });
        }
    });

}



function setPoiVisible(namepoi) {

    map.getLayers().forEach(function (layer, i) {

        // bindInputs('#layer' + i, layer);
        if (layer instanceof ol.layer.Group) {
            // console.log("Group Name is : " + layer.getProperties().name)
            layer.getLayers().forEach(function (sublayer, i) {

                // map.removeLayer(layer);
                if (sublayer.getProperties().name === namepoi) {

                    if(sublayer.getVisible(true)){

                        sublayer.setVisible(false);

                    }
                    else {
                        sublayer.setVisible(true);
                    }


                }


            });
        }
    });

}




function poiExist(poiName){

    var itExists = false;
    // check if poi is already created if so skip and make visible instead
        map.getLayers().forEach(function (layer, i) {

        if (layer instanceof ol.layer.Group) {
            // console.log("Group Name is : " + layer.getProperties().name)
            layer.getLayers().forEach(function (sublayer, i) {

                if (sublayer.getProperties().name === poiName) {
                    itExists = true;

                }

            });
        }
    });

    return itExists;

}



function searchPoi(campusId, searchString) {


       if (poiExist(searchString)){


        setPoiVisible(searchString);

    }


// testCreatePoi("Entrance")
// testCreatePoi("Info Point")
    // removePoi(poiLayer);


    else {

            // var searchUrl = '/api/v1/buildings/' + buildingId + '/' + spaceName + '.json';
        // var searchUrl = baseApiUrl + 'campus/' + campusId + '/search/' + searchString + '?format=json';
        var searchUrl = baseApiUrl + "campus/1/poi/name/" + searchString + '/?format=json';
        console.log("in searchPOI: " + searchUrl);

       // create the poi because it does not exist
            var poiSource = new ol.source.Vector();
        $.ajax(searchUrl).then(function (response) {
            console.log("in response: " + response);
            var geojsonFormat3 = new ol.format.GeoJSON();
            var featuresSearch = geojsonFormat3.readFeatures(response,
                {featureProjection: 'EPSG:4326'});
            poiSource.addFeatures(featuresSearch);

            // zoomToFeature(searchSource);


            var centerCoord = ol.extent.getCenter(poiSource.getExtent());
            console.log(centerCoord);

            //open_popup(featuresSearch[0].getProperties(), centerCoord);

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
            name: "nice icon",
            population: 4000,
            rainfall: 500
        });

        var iconStyle = new ol.style.Style({
            image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
                anchor: [0.5, 46],
                anchorXUnits: 'fraction',
                anchorYUnits: 'pixels',
                src: '/static/access_parking_bikecovered.png'
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
            source: poiSource,
            style: iconStyle,
            title: "foo",
            name: searchString,
            active: true,
            visible: true,
            zIndex: 999
        });


        return poiLayer;


    }




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