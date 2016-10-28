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


function setPoiVisibility(namepoi) {

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


function getPoiIcon(poiName){

    // poiIconImage = '/static/homepage/img/' + poiName + '.png'
    poiIconImage = '/static/homepage/img/access_parking_bikecovered.png'

    return poiIconImage;
}


function createPoiStyle(poiName){

        var iconStyle = new ol.style.Style({
            image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
                anchor: [0.5, 46],
                anchorXUnits: 'fraction',
                anchorYUnits: 'pixels',
                src: getPoiIcon(poiName)
            }))
        });

        return iconStyle;
}


function createPoi(campusId, poiName) {

    if (poiExist(poiName)){
        // do nothing

    } else {

        var poiUrl = baseApiUrl + "campus/1/poi/name/" + poiName + '/?format=json';
        console.log("in createPoi: " + poiUrl);

        // create the poi because it does not exist
        var poiSource = new ol.source.Vector();
        $.ajax(poiUrl).then(function (response) {
            console.log("in response: " + response);
            var geojsonFormat3 = new ol.format.GeoJSON();
            var featuresSearch = geojsonFormat3.readFeatures(response,
                {featureProjection: 'EPSG:4326'});
            poiSource.addFeatures(featuresSearch);

        });

        poiVectorLayer = new ol.layer.Vector({
            source: poiSource,
            style: createPoiStyle(poiName),
            title: poiName,
            name: poiName,
            active: true,
            visible: true,
            zIndex: 999
        });

        poiLayerGroup.getLayers().push(poiVectorLayer);

        return poiVectorLayer;
    }


}


function searchPoi(campusId, searchString) {


   if (poiExist(searchString)){

        setPoiVisibility(searchString);

    }
    else {

       var finally_a_poi = createPoi(1, searchString);

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
            // var searchResFloorNum = featuresSearch[0].getProperties().floor_num;
            // for (var i = 0; i < switchableLayers.length; i++) {
            //     if (searchResFloorNum == switchableLayers[i].getProperties().floor_num) {
            //         activateLayer(i);
            //     }
            // }


        });


        poiLayer = new ol.layer.Vector({
            source: poiSource,
            style: createPoiStyle(searchString),
            title: "foo",
            name: searchString,
            active: true,
            visible: true,
            zIndex: 999
        });

        return poiLayer;
       //return finally_a_poi;

    }

}



$('#kiosk-pois a').click(function() {

    var poiName = $(this).attr('id').split('_')[1];
    var elemId = $(this).attr('id');

    if (poiExist(poiName)){

        setPoiVisibility(poiName);
        $(elemId).addClass("active");

    }
    else {
        var newPoi = createPoi(1,poiName);
        map.getLayers().push(newPoi);



    }


});

