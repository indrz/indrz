map.on('moveend', function (e) {
    update_url('map');
});

function update_url(mode) {

    var current_extent2 = map.getView().calculateExtent(map.getSize());
    var current_zoom2 = map.getView().getZoom();
    var center_crd = map.getView().getCenter();
    var centerx2 = center_crd[0];
    var centery2 = center_crd[1];

    var url = "/map/" + map_name + "/?buildingid=" + building_id +
        "&centerx=" + centerx2 + "&centery=" + centery2 + "&zlevel=" + current_zoom2 +
        "&floor=" + active_floor_num;

    var data = {};

    if (mode == "route") {
        url = "/map/" + map_name + "/?buildingid=" + building_id + "&route_from=" + $("#route-from").val() + "&route_to=" + $("#route-to").val();
    } else if (mode == "search") {
        url = "/map/" + map_name + "/?buildingid=" + building_id + "&spaceid=" + space_id;
    } else if (mode == "map") {
        url = "/map/" + map_name + "/?buildingid=" + building_id +
            "&centerx=" + centerx2 + "&centery=" + centery2 + "&zlevel=" + current_zoom2 +
            "&floor=" + active_floor_num;
    }

    data.extent = current_extent2;
    data.zoom = current_zoom2;
    history.pushState(data, 'live_url_update', url);
}


window.addEventListener('popstate', function (event) {
    updateContent(event.state);
});

function updateContent(data) {
    if (data == null)
        return;
}
