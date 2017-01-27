var routeLayer = null;
var markerLayer = null;

var start_maker_style = new ol.style.Style({
    image: new ol.style.Icon({
        src: '/static/img/route_start.png'
    })
});
var end_maker_style = new ol.style.Style({
    image: new ol.style.Icon({
        src: '/static/img/route_end.png'
    })
});


var route_active_style = new ol.style.Style({
    stroke: new ol.style.Stroke({
        color: 'red',
        width: 4
    })
});

var route_inactive_style = new ol.style.Style({
    stroke: new ol.style.Stroke({
        color: 'red',
        width: 2,
        lineDash: [0.1, 5],
        opacity: 0.5
    })
});


// function getDirections(){
//
//     var customer = {contact_name :"Scott",company_name:"HP"};
//     $.ajax({
//         type: "POST",
//         data :JSON.stringify(customer),
//         url: "api/Customer",
//         contentType: "application/json"
//     });
//
// }


// function getDirections2(xStart, yStart, floorStart, xEnd, yEnd,endFloor, routeType) {
function getDirections2(startSearchText, endSearchText, routeType) {


    // var startVals = get_start(startSearchText);
    // var endVals = get_start(endSearchText);


    // var geoJsonUrl = baseApiRoutingUrl + 'start_coord=' + aksStart + '&endstr=' + aksEnd + '/?format=json';
    //
    // var routeUrl = baseApiRoutingUrl + "1826657.11148431,6142529.11906656,4&1826685.08369027,6142499.12539894,4&1"
    // var geoJsonUrl = baseApiRoutingUrl + xStart + "," + yStart + "," + floorStart + "&" + xEnd + "," + yEnd + "," + endFloor + "&" + routeType;
    //var geoJsonUrl = baseApiRoutingUrl + startVals + "&" + endVals + "&" + 0;
    // var geoJsonUrl = baseApiRoutingUrl + 'start_coord=' + routeLocalData.start.routeValue + '&enstr='+ routeLocalData.end.routeValue + '/?format=json';

var geoJsonUrl = baseApiRoutingUrl + startSearchText + "&" + endSearchText + "&" + routeType + '/?format=json';


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

$("#clearRoute").click(function () {
    if (routeLayer) {
        map.removeLayer(routeLayer);
    }
    if (markerLayer) {
        map.removeLayer(markerLayer);
    }
    $("#clearRoute").addClass("hide");
    $("#shareRoute").addClass("hide");
    $("#route-to").val('');
    $("#route-from").val('');
});

function addMarkers(route_features){
    var marker_features = [];
    var lengthList = [];
    var floorList = [];
    var prevFloorNum = -99;
    var index = -1;
    var nFeatures = route_features.length;
    var distance = 0;

    if(markerLayer){
        map.removeLayer(markerLayer);
    }

    if(nFeatures == 0 ) return;
    // add middle icons
    for(var i = 0; i < nFeatures; i++) {
        var floor_num = route_features[i].getProperties().floor;
        if (prevFloorNum != floor_num) {
            floorList.push(floor_num);
            index++;
            prevFloorNum = floor_num;
            if (!lengthList[index]) lengthList[index] = 0;
        }
        lengthList[index] += route_features[i].getGeometry().getLength();
    }

    index = 0;
    for(i = 0; i < nFeatures; i++){
        var floor_num = route_features[i].getProperties().floor;

        if(floorList[index]==floor_num)
            distance += route_features[i].getGeometry().getLength();
        if(floorList[index]==floor_num && lengthList[index]/2 < distance){
            var line_extent = route_features[i].getGeometry().getExtent();
            var middleCoordinate = ol.extent.getCenter(line_extent);
            var middlePoint = new ol.geom.Point(route_features[i].getGeometry().getClosestPoint(middleCoordinate));

            var middleFeature = new ol.Feature({
                geometry: middlePoint
            });
            var floor_num_style = new ol.style.Style({
                image: new ol.style.Icon({
                    src: '/static/img/route_floor_' + floor_num + '.png'
                })
            });
            middleFeature.setStyle(floor_num_style);
            marker_features.push(middleFeature);

            index ++;
            distance = 0;
        }

    }

    // Add start/end marker
    var start_point = new ol.geom.Point(route_features[0].getGeometry().getLastCoordinate());
    var end_point = new ol.geom.Point(route_features[route_features.length-1].getGeometry().getLastCoordinate());
    var startMarker = new ol.Feature({
        geometry: start_point
    });
    var endMarker = new ol.Feature({
        geometry: end_point
    });
    endMarker.setGeometry(end_point);
    startMarker.setStyle(start_maker_style);
    endMarker.setStyle(end_maker_style);

    marker_features.push(startMarker);
    marker_features.push(endMarker);

    markerLayer = new ol.layer.Vector({
        source: new ol.source.Vector({
          features: marker_features
        }),
        title: "icon_layer",
        name: "icon_layer",
        visible: true,
        zIndex: 9999
    });
    map.getLayers().push(markerLayer);
}

function routeToNearestPoi(startXY, floorNum, poiCatId){


    var geoJsonUrl = baseApiRoutingUrl + 'startxy=' + startXY + '&floor=' + floorNum + '&poiCatId=' + poiCatId + '/?format=json';

    //
    // $.getJSON(geoJsonUrl, function(json){
    //     destinationPoiInfo = json.route_info[0].destination.name;
    // });

       // var myD =  $.getJSON(geoJsonUrl, function(data) {
       //                   var n = data.route_info[0].destination.name;
       //                  console.log("xxxxxxxxx x  :  " + n);
       //
       //                  destinationPoiInfo.push(n);
       //
       //                  return n
       //                  //data is the JSON string
       //              });

       // console.log("PPPPPPPPPPPPPPPPP " + destinationPoiInfo);
       //
       // document.getElementById('route-to').value = destinationPoiInfo;


    if (routeLayer) {
        map.removeLayer(routeLayer);
        console.log("removing layer now");
        //map.getLayers().pop();
    }

    var source = new ol.source.Vector();
    $.ajax(geoJsonUrl).then(function (response) {
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