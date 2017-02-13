

// valid startSearchText string is 21315.12,12312.123,3   x,y,floor_num
function getDirectionsFromKiosk(endSearchText, routeType) {

    // http://localhost:8000/indrz/api/v1/kiosk/route/irene%20fellner

    // var geoJsonUrl = baseApiRoutingUrl + startSearchText + "&" + endSearchText + "&" + routeType + '/?format=json';
    var geoJsonUrl = '/indrz/api/v1/kiosk/route/' + endSearchText ;
    var startingLevel = routeType;

    if (routeLayer) {
        map.removeLayer(routeLayer);
        console.log("removing layer now");
        //map.getLayers().pop();
    }

    var source = new ol.source.Vector();
    $.ajax(geoJsonUrl).then(function (response) {
        //console.log("response", response);
        var geojsonFormat = new ol.format.GeoJSON();
        var features = geojsonFormat.readFeatures(response,
            {featureProjection: 'EPSG:4326'});
        source.addFeatures(features);

        addMarkers(features);

        // active the floor of the start point
        var start_floor = features[0].getProperties().floor;
        for (var i = 0; i < floor_layers.length; i++) {
            if (start_floor == floor_layers[i].floor_num) {
                activateLayer(i);
            }
        }
        // center up the route
        var extent = source.getExtent();
        map.getView().fit(extent, map.getSize());
    });

    routeLayer = new ol.layer.Vector({
        //url: geoJsonUrl,
        //format: new ol.format.GeoJSON(),
        source: source,
        style: function (feature, resolution) {
            var feature_floor = feature.getProperties().floor;
            if (feature_floor == active_floor_num) {
                feature.setStyle(route_active_style);
            } else {
                feature.setStyle(route_inactive_style);
            }
        },
        title: "Route",
        name: "Route",
        visible: true,
        zIndex: 9999
    });

    map.getLayers().push(routeLayer);

    $("#clearRoute").removeClass("hide");
    $("#shareRoute").removeClass("hide");

}


function addRoute(fromSearchText, toSearchText, routeType) {
    var geoJsonUrl = baseApiRoutingUrl + 'startstr=' + fromSearchText + '&endstr=' + toSearchText + '/?format=json';

    var startingLevel = fromSearchText.charAt(0);

    if (routeLayer) {
        map.removeLayer(routeLayer);
        console.log("removing layer now");
        //map.getLayers().pop();
    }

    var source = new ol.source.Vector();
    $.ajax(geoJsonUrl).then(function (response) {
        //console.log("response", response);
        var geojsonFormat = new ol.format.GeoJSON();
        var features = geojsonFormat.readFeatures(response,
            {featureProjection: 'EPSG:4326'});
        source.addFeatures(features);

        addMarkers(features);

        // active the floor of the start point
        var start_floor = features[0].getProperties().floor;
        for (var i = 0; i < floor_layers.length; i++) {
            if (start_floor == floor_layers[i].getProperties().floor_num) {
                activateLayer(i);
            }
        }
        // center up the route
        var extent = source.getExtent();
        map.getView().fit(extent, map.getSize());
    });

    routeLayer = new ol.layer.Vector({
        //url: geoJsonUrl,
        //format: new ol.format.GeoJSON(),
        source: source,
        style: function (feature, resolution) {
            var feature_floor = feature.getProperties().floor;
            if (feature_floor == active_floor_num) {
                feature.setStyle(route_active_style);
            } else {
                feature.setStyle(route_inactive_style);
            }
        },
        title: "Route",
        name: "Route",
        visible: true,
        zIndex: 9999
    });

    map.getLayers().push(routeLayer);

    $("#clearRoute").removeClass("hide");
    $("#shareRoute").removeClass("hide");
}
