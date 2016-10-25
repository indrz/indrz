var searchLayer = null;


var search_res_style = new ol.style.Style({
    fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 0.6)'
    }),
    stroke: new ol.style.Stroke({
        color: '#319FD3',
        width: 2
    }),
    text: new ol.style.Text({
        font: 'bold 12px Arial,sans-serif',
        fill: new ol.style.Fill({
            color: '#000'
        }),
        maxResolution: 2000,
        stroke: new ol.style.Stroke({
            color: '#fff',
            width: 3
        })
    })
});


function setSearchFeatureStyle(feature, resolution) {
    if (feature) {

        if (feature.get('short_name') !== null) {
            //info.innerHTML = feature.getId() + ': ' + feature.get('name');
            search_res_style.getText().setText(resolution < 0.1 ? feature.get('short_name') : '');
            return [search_res_style];

        }
    }

}

function zoomToFeature(source) {

    var view = map.getView();
    // view.setCenter([centerx, centery]);
    view.setZoom(19);

    var feature = source.getFeatures()[0];
    var polygon = /** @type {ol.geom.SimpleGeometry} */ (feature.getGeometry());
    var size = /** @type {ol.Size} */ (map.getSize());
    view.fit(polygon, size, {padding: [170, 50, 30, 150], constrainResolution: false})

    // view.fit(polygon, size, {padding: [170, 50, 30, 150], nearest: true})}
    // view.fit(point, size, {padding: [170, 50, 30, 150], minResolution: 50})}
    }


function zoomer(coord, zoom){
        var pan = ol.animation.pan({
          duration: 2000,
          source: /** @type {ol.Coordinate} */ (view.getCenter())
        });
        map.beforeRender(pan);

        view.setCenter(coord);
       // view.setZoom(zoom)
    }

function searchIndrz(campusId, searchString) {
    // var searchUrl = '/api/v1/buildings/' + buildingId + '/' + spaceName + '.json';
    // var searchUrl = baseApiUrl + 'campus/' + campusId + '/search/' + searchString + '?format=json';
    var searchUrl = '/search/' + searchString + '?format=json';

    if (searchLayer) {
        map.removeLayer(searchLayer);
        console.log("removing search layer now");
        //map.getLayers().pop();
    }


    var searchSource = new ol.source.Vector();
    $.ajax(searchUrl).then(function (response) {
        var geojsonFormat3 = new ol.format.GeoJSON();
        var featuresSearch = geojsonFormat3.readFeatures(response,
            {featureProjection: 'EPSG:4326'});
        searchSource.addFeatures(featuresSearch);

        // zoomToFeature(searchSource);


        var centerCoord = ol.extent.getCenter(searchSource.getExtent());
        console.log(centerCoord);

        // zoomer(centerCoord, 20);
       // zoomToFeature(searchSource);
       // zoomer(centerCoord);
        // view = map.getView();
        // view.setCenter(centerCoord);
        // console.log("setting popup center to "+  centerCoord)
        // view.setZoom(20);


        open_popup(featuresSearch[0].getProperties(), centerCoord);

        space_id = response.features[0].properties.space_id;

        // active the floor of the start point
        var searchResFloorNum = featuresSearch[0].getProperties().floor_num;
        for (var i = 0; i < switchableLayers.length; i++) {
            if (searchResFloorNum == switchableLayers[i].getProperties().floor_num) {
                activateLayer(i);
            }
        }

    });


    searchLayer = new ol.layer.Vector({
        source: searchSource,
        style: setSearchFeatureStyle,
        title: "SearchLayer",
        name: "SearchLayer",
        zIndex: 999
    });

    map.getLayers().push(searchLayer);
    $("#clearSearch").removeClass("hide");
    $("#shareSearch").removeClass("hide");

}

$("#clearSearch").click(function () {
    if (searchLayer) {
        map.removeLayer(searchLayer);
    }
    close_popup();

    $("#clearSearch").addClass("hide");
    $("#shareSearch").addClass("hide");
    $("#search-input").val('');

});