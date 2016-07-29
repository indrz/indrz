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


function searchIndrz(buildingId, spaceName) {
    var searchUrl = '/api/v1/buildings/' + buildingId + '/' + spaceName + '.json';

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
        //var searchFloorId = featuresSearch[0].getProperties().fk_building_floor.id;
        map.getView().setCenter(ol.extent.getCenter(searchSource.getExtent()));
        map.getView().setZoom(21);
        //waitForFloors(searchFloorId);

        var centerCoord = ol.extent.getCenter(searchSource.getExtent());
        open_popup(featuresSearch[0].getProperties(), centerCoord);

        space_id = response.features[0].id;

        // active the floor of the start point
        var searchResFloorNum = featuresSearch[0].getProperties().floor_num;
        for (var i = 0; i < floor_layers.length; i++) {
            if (searchResFloorNum == floor_layers[i].getProperties().floor_num) {
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

}

$("#clearSearch").click(function () {
    if (searchLayer) {
        map.removeLayer(searchLayer);
    }
    close_popup();

    $("#clearSearch").addClass("hide");
    $("#search-input").val('');

});
var searchPanelShown = true;
$("#toggle-search").click(function () {
    if (searchPanelShown) {
        var panelWidth = $("#search-panel").outerWidth();
        var buttonWidth = $("#toggle-search").outerWidth();
        var leftPosition = -(panelWidth - buttonWidth);
        $("#search-panel").css("left", leftPosition+"px");
    } else {
         $("#search-panel").css("left", "0");
    }
    searchPanelShown = !searchPanelShown;
    //$("#search-panel").toggleClass("minimized");
    $("#toggle-search i").toggleClass("fa-chevron-left").toggleClass("fa-chevron-right");
});