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


function getLayerGroupByName() {


    map.getLayers().forEach(function (layer, i) {

        // bindInputs('#layer' + i, layer);
        if (layer instanceof ol.layer.Group) {

            if(layer.getProperties().name === 'poi group'){

                console.log("Group Name is : " + layer.getProperties().name)
                var poi_groupLayer = layer.getLayers();
                return poi_groupLayer;

            }



        }
    });

}


function listActivePoiLayers() {

    var poiStatus = false;

    map.getLayers().forEach(function (layer, i) {

        // bindInputs('#layer' + i, layer);
        if (layer instanceof ol.layer.Group) {
            // console.log("Group Name is : " + layer.getProperties().name)

            if(layer.getProperties().name === "poi group"){

                return
                layer.getLayers().forEach(function (sublayer, i) {

                    // console.log("POI Layer Name is : " + sublayer.getProperties().name)

                    poiStatus = true;
                    return poiStatus;

                    });

            }
            else{
                // console.log("no active pois on map");
                return poiStatus;
            }


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


function createPoiStyle(poiIconName, active){

    poiIconImageHidden = '/static/homepage/img/access_parking_p1.png'
    poiIconImage = '/static/homepage/img/' + poiIconName + '.png'



    var iconDeactiveStyle = new ol.style.Style({
        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
            anchor: [0.5, 46],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: poiIconImageHidden
        }))
    });

    var iconStyle = new ol.style.Style({
        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
            anchor: [0.5, 46],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: poiIconImage
        }))
    });

    if (active==='y'){

        return iconStyle;
    }
    else {

        return iconDeactiveStyle;
    }

}


function createPoi(campusId, poiName, poiCatId, poiIconName) {

    if (poiExist(poiName)){
        // do nothing

    } else {

        var poiUrl = baseApiUrl + "campus/1/poi/poi/cat/" + poiCatId + '/?format=json';
        console.log("in createPoi: " + poiUrl);

        console.log( $( "li" ).get( 0 ) );

        // create the poi because it does not exist
        var poiSource = new ol.source.Vector();

        $.ajax(poiUrl).then(function (response) {
            // console.log("in response: " + response);
            var geojsonFormat3 = new ol.format.GeoJSON();
            var featuresSearch = geojsonFormat3.readFeatures(response,
                {featureProjection: 'EPSG:4326'});
            poiSource.addFeatures(featuresSearch);

        });

        var poiVectorLayer = new ol.layer.Vector({
            source: poiSource,
            style: createPoiStyle(poiIconName, 'y'),
            // style: function (feature, resolution) {
            //
            //     var poiFeature_floor = feature.getProperties().floor_num;
            //     if (poiFeature_floor == active_floor_num) {
            //         feature.setStyle(createPoiStyle(poiIconName, 'y'));
            //     } else {
            //         feature.setStyle(createPoiStyle(poiIconName, 'n'));
            //     }
            // },
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


$('#kiosk-pois a').click(function() {

    var poiCatName = $(this).attr('id').split('_')[0];
    var poiCatId = $(this).attr('id').split('_')[1];
    var className = $('.myclass').attr('class');
    var poiIconName = $('#kiosk-pois a > img').attr('class');

    if (poiExist(poiCatName)){

        setPoiVisibility(poiCatName);
        $(poiCatId).addClass("active");

    }
    else {
        var newPoi = createPoi(1,poiCatName, poiCatId, poiIconName);
        map.getLayers().push(newPoi);

    }


});

