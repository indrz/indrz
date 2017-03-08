function library_book_position(foo) {
    return $.ajax({
        dataType: 'json',
        url: '/indrz/api/v1/library/location/' + foo
    }).done(function (data) {
        // If successful

        routeLocalData.start = {};
        routeLocalData.start.xcoord = 1826545.2173675;
        routeLocalData.start.ycoord = 6142423.4241214;
        routeLocalData.start.floor = 0;
        var routeStartValue = routeLocalData.start.xcoord + "," + routeLocalData.start.ycoord + "," + routeLocalData.start.floor;

        routeLocalData.start.routeValue = routeStartValue;
        routeLocalData.end = {};
        // console.log(JSON.stringify(data));
        routeLocalData.end.xcoord = data.geometry.coordinates[0];
        routeLocalData.end.ycoord = data.geometry.coordinates[1];
        routeLocalData.end.floor = data.properties.floor_num;

        var routeEndValue = routeLocalData.end.xcoord + "," + routeLocalData.end.ycoord + "," + routeLocalData.end.floor;

        routeLocalData.end.routeValue = routeEndValue;

        getDirections2(routeStartValue, routeEndValue, 0);

        var popup_location = [data.geometry.coordinates[0]];
        popup_location.push(data.geometry.coordinates[1]);
        console.log("popuploacation is : " + popup_location);
        console.log("coords  is : " + data.geometry.coordiantes);
        console.log("props  is : " + data.properties);

        // TODO make library popup look good
        // uncomment to activate it works but looks bad
        //open_popup(data.properties, popup_location, data.properties.name );


    }).fail(function (jqXHR, textStatus, errorThrown) {
        // If fail
        //console.log(textStatus + ': ' + errorThrown);
    });
}


// var createLibraryPopup = function (geometry, floor, building, fachboden, shelfID, rvk_key) {
//     //replace %20 with space
//     var key = rvk_key.split("%20").join(" ");
//     // zoom to feature
//     // removed fachboden icon show <tr align="center"><td colspan="2"><img height="35" width="35" src="img/lib_fachboden_'+fachboden+'.png"/></td></tr>
//     var contentHtml =
//         '<table width="100%" height="100%">' +
//         '<tr><td align="left"><b>' + $.t('library.building') + ':</b></td>' +
//         '<td align="left"><b>' + building + '</b></td></tr><tr>' +
//         '<td align="left"><b>' + $.t('routing.floor') + ':</b></td>' +
//         '<td align="left"><b>' + floor + '</b></td></tr><tr>' +
//         // '<td align="left"><b>'+$.t('library.shelf')+':</b></td>' +
//         // '<td align="left"><b>'+shelfID+'</b></td></tr><tr>' +
//         '<td align="left"><b>RVK:</b></td>' +
//         '<td align="left"><b>' + key + '</b></td></tr>' +
//         //'<tr><td colspan="2" align="center"><a href="http://www.wu.ac.at/library">'+ $.t("library.backToSearch")+'</a></td></tr>' +
//         '</table></td></tr></table>'
//
//     popupLocationGeom = getGeomWithPXOffset(geometry, 100, 0);
//
//     AppMain.viewer.tools['routingModule'].routingControl.libraryPopup = new GeoExt.Popup({
//         id: 'infoPopup',
//         title: $.t('library.popup_title'),
//         html: '<div id="libraryPopup">' + contentHtml + '</div>',
//         collapsible: true,
//         resizable: false,
//         draggable: true,
//         anchorPosition: 'bottom-right',
//         // location: geometry,
//         location: popupLocationGeom,
//         map: AppMain.viewer.mapPanel,
//         popupCls: "x-window-draggable"
//     });
//
//
//     AppMain.viewer.tools['routingModule'].routingControl.libraryPopup.show();
//
//
// };
//
// var destroyLibraryPopup = function () {
//     if (AppMain.viewer.tools['routingModule'].routingControl.libraryPopup != undefined) {
//         AppMain.viewer.tools['routingModule'].routingControl.libraryPopup.destroy();
//         AppMain.viewer.tools['routingModule'].routingControl.libraryPopup = undefined;
//     }
// };

// var calculateRouteToShelf = function (geo, floor) {
// var shelf_Middle = geo[0].geometry.getCentroid();
//
// AppMain.viewer.tools['routingModule'].addRouteStartPoint(1826545.2173675, 6142423.4241214, $.t('library.routeStart'), 0);
// AppMain.viewer.tools['routingModule'].addRouteEndPoint(shelf_Middle.x, shelf_Middle.y, $.t('library.routeEnd'), floor);
//
// //switch floor and center
// AppMain.viewer.tools['routingModule'].routingControl.centerTo(shelf_Middle.x, shelf_Middle.y, 22);
// AppMain.changeFloorTo(floor);

// function RouteToShelf(rvk_id) {
//     // request, start_coord, start_floor, end_coord, end_floor, route_type):
//     //http:/localhost:8000/api/v1/directions/1587848.414,5879564.080,2&1588005.547,5879736.039,2&0
//
//     var baseUrl = '/api/v1/library/route/';
//     var geoJsonUrl = baseUrl + rvk_id;
//
//
//     if (routeLayer) {
//         map.removeLayer(routeLayer);
//         console.log("removing layer now");
//         //map.getLayers().pop();
//     }
//
//     var source = new ol.source.Vector();
//     $.ajax(geoJsonUrl).then(function (response) {
//         //console.log("response", response);
//         var geojsonFormat = new ol.format.GeoJSON();
//         var features = geojsonFormat.readFeatures(response,
//             {featureProjection: 'EPSG:4326'});
//         source.addFeatures(features);
//
//         addMarkers(features);
//
//         // active the floor of the start point
//         var start_floor = features[0].getProperties().floor;
//         for (var i = 0; i < switchableLayers.length; i++) {
//             if (start_floor == switchableLayers[i].getProperties().floor_num) {
//                 activateLayer(i);
//             }
//         }
//         // center up the route
//         var extent = source.getExtent();
//         map.getView().fit(extent, map.getSize());
//     });
//
//     routeLayer = new ol.layer.Vector({
//         //url: geoJsonUrl,
//         //format: new ol.format.GeoJSON(),
//         source: source,
//         style: function (feature, resolution) {
//             var feature_floor = feature.getProperties().floor;
//             if (feature_floor == active_floor_num) {
//                 feature.setStyle(route_active_style);
//             } else {
//                 feature.setStyle(route_inactive_style);
//             }
//         },
//         title: "Route",
//         name: "Route",
//         visible: true,
//         zIndex: 9999
//     });
//
//     map.getLayers().push(routeLayer);
//
//     $("#clearRoute").removeClass("hide");
//     $("#shareRoute").removeClass("hide");
//
// }
//
// var unanchorPopup = function (popup) {
//     popup.removeAnchorEvents();
//
//     //make the window draggable
//     popup.draggable = true;
//     popup.header.addClass("x-window-draggable");
//     popup.dd = new Ext.Window.DD(popup);
//
//     //remove anchor
//     popup.anc.remove();
//     popup.anc = null;
//
//     //hide unpin tool
//     popup.tools.unpin.hide();
// };


/*
 returns a new geom with pixel offset. has to be in 900973 format
 point should be  OpenLayers.Geometry.Point
 xOff and yOff are in Pixels
 */
// var getGeomWithPXOffset = function (point, xOff, yOff) {
//     var x = point.x;
//     var y = point.y;
//
//     console.log(AppMain);
//
//     var location = AppMain.viewer.tools['routingModule'].routingControl.map.getPixelFromLonLat(new OpenLayers.LonLat(x, y));
//
//     location.x += xOff;
//     location.y += yOff;
//
//     var locationLonLat = AppMain.viewer.tools['routingModule'].routingControl.map.getLonLatFromLayerPx(location);
//
//     return new OpenLayers.Geometry.Point(locationLonLat.lon, locationLonLat.lat);
// };
// ;