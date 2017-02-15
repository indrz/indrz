function searchIndrzKiosk(campusId, searchString) {
    // var searchUrl = '/api/v1/buildings/' + buildingId + '/' + spaceName + '.json';
    // var searchUrl = baseApiUrl + 'campus/' + campusId + '/search/' + searchString + '?format=json';
    var searchUrl = '/search/' + searchString + '?format=json';

    if (searchLayer) {
        map.removeLayer(searchLayer);
        clearSearchResults();
        $("#search-input-kiosk").val('');

    }

    if (routeLayer) {
        map.removeLayer(routeLayer);

        //map.getLayers().pop();
    }



    var searchSource = new ol.source.Vector();
    $.ajax(searchUrl).then(function (response) {
        var geojsonFormat3 = new ol.format.GeoJSON();
        var featuresSearch = geojsonFormat3.readFeatures(response,
            {featureProjection: 'EPSG:4326'});
        searchSource.addFeatures(featuresSearch);

        searchSource.forEachFeature(function(feature) {

            var att = feature.get("name");
            var floor = feature.get("floor_num");
            var roomcat = feature.get('category_de');
            var roomcode = feature.get('roomcode');
            var infoo = '"' + att + '"'
            if (roomcat != "" && roomcat != undefined){
                var htmlInsert = "<a href='#' onclick='showResKiosk(" + infoo + ")' id='searchResListItem_"+ att +
                "' class='list-group-item indrz-search-res' >" + att +" ("+ roomcat + ") <span class='badge'>"+ gettext('Floor  ') + floor +"</span> </a>"
            }
            else if (roomcode != "" && roomcode != undefined){
                var htmlInsert = "<a href='#' onclick='showResKiosk(" + infoo + ")' id='searchResListItem_"+ att +
                "' class='list-group-item indrz-search-res' >" + att +" ("+ roomcode + ") <span class='badge'>"+ gettext('Floor  ') + floor +"</span> </a>"
            }
            else{
                 var htmlInsert = "<a href='#' onclick='showResKiosk(" + infoo + ")' id='searchResListItem_"+ att +
                "' class='list-group-item indrz-search-res' >" + att + " <span class='badge'>"+ gettext('Floor  ') + floor +"</span> </a>"
            }




            $("#search-results-list").append(htmlInsert);
            });


        var centerCoord = ol.extent.getCenter(searchSource.getExtent());

        if (featuresSearch.length === 1){
            var featName = featuresSearch[0].getProperties().name;

            open_popup(featuresSearch[0].getProperties(), centerCoord);
            getDirectionsFromKiosk(featName, 0);

        }

        space_id = response.features[0].properties.space_id;
        poi_id = response.features[0].properties.poi_id;
        search_text = searchString;

        // active the floor of the start point
        activateFloor(featuresSearch[0]);

    } );


    searchLayer = new ol.layer.Vector({
        source: searchSource,
        style: styleFunction,
        title: "SearchLayer",
        name: "SearchLayer",
        zIndex: 999
    });

    map.getLayers().push(searchLayer);

    $("#search-res").removeClass("hide");
    $("#clearSearch").removeClass("hide");
    $("#shareSearch").removeClass("hide");

}

function showResKiosk(featureName){
    searchLayer.getSource().forEachFeature(function(feature) {
        if (feature.get('name') === featureName ){
            open_popup(feature.getProperties(), feature.get('centerGeometry').coordinates);
            getDirectionsFromKiosk(featureName, 0);

            activateFloor(feature);

        }

    })


}