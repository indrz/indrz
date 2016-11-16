map.on('moveend', function (e) {
    update_url('map');
});

function update_url(mode) {

    var current_extent2 = map.getView().calculateExtent(map.getSize());
    var current_zoom2 = map.getView().getZoom();
    var center_crd = map.getView().getCenter();
    var centerx2 = center_crd[0];
    var centery2 = center_crd[1];

    var url = "/?campus=" + building_id + "&centerx=" + centerx2 + "&centery=" + centery2 +
        "&zlevel=" + current_zoom2 + "&floor=" + active_floor_num;

    // var url = "/map/" + map_name + "/?campus=" + building_id +
    //     "&centerx=" + centerx2 + "&centery=" + centery2 + "&zlevel=" + current_zoom2 +
    //     "&floor=" + active_floor_num;

    var data = {};

    // if (mode == "route") {
    //     url = "/map/" + map_name + "/?campus=" + building_id + "&startstr=" + $("#route-from").val() + "&endstr=" + $("#route-to").val();
    // } else if (mode == "search") {
    //     url = "/map/" + map_name + "/?campus=" + building_id + "&spaceid=" + space_id;
    // } else if (mode == "map") {
    //     url = "/map/" + map_name + "/?campus=" + building_id + "&centerx=" + centerx2 + "&centery=" + centery2 + "&zlevel=" + current_zoom2 + "&floor=" + active_floor_num;
    // }

    if (mode == "route") {
        url = "/?campus=" + building_id + "&startstr=" + $("#route-from").val() + "&endstr=" + $("#route-to").val();
    } else if (mode == "search") {

        // if(poi_id > 0){
        //     url = "/?campus=" + building_id + "&poi-id=" + poi_id;
        // }
        // if(space_id > 0){
        //     url = "/?campus=" + building_id + "&spaceid=" + space_id;
        // }

        if(search_text != undefined && search_text != ""){
            url = "/?campus=" + building_id + "&q=" + search_text;
        }
        // url = "/?campus=" + building_id + "&spaceid=" + share_xy;
        // url = "/?campus=" + building_id + "&spaceid=" + share_xy;
        // url = "/?campus=" + building_id + "&share_xy=" + "[" + share_xy + "]";
    //    http://localhost:8000/?campus=1&share_xy=%22[1826602.52731,6142514.228525]
    } else if (mode == "map") {
        url = "/?campus=" + building_id + "&centerx=" + centerx2 + "&centery=" + centery2 + "&zlevel=" + current_zoom2 + "&floor=" + active_floor_num;
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
