var switchableLayers = [wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03, wmsE04, wmsE05, wmsE06];

function waitForFloors(space_floor_id) {
    if (floor_layers.length > 0) {

        // for (var i = 0; i < floors_info.length; ++i) {
        //     floor_layers.push(floors_info[i]);
        //     appendFloorNav(floors_info[i].short_name, [i]);
        //     }

        activateLayer(space_floor_id);


        // for (var i = 0; i < building_info.num_floors; i++) {
        //     if (building_info.buildingfloor_set[i].id == space_floor_id) {
        //         activateLayer(i);
        //     }
        // }
    }
    else {
        setTimeout(function () {
            waitForFloors(space_floor_id);
        }, 250);
    }
}


function hideLayers() {
    for (var i = 0; i < switchableLayers.length; i++) {
        switchableLayers[i].setVisible(false);
    }
    // if (floor_layers.length > 0) {
    //     for (var i = 0; i < floor_layers.length; i++) {
    //         floor_layers[i].setVisible(false);
    //     }
    // }
    $("#floor-links li").removeClass("active");
}


function setLayerVisible(index) {
    // switchableLayers[index].setVisible(true);
    if (switchableLayers.length > 0) {
        switchableLayers[index].setVisible(true);
        $("#floor-links li:nth-child(" + (switchableLayers.length - index) + ")").addClass("active");

        // set active_floor_num
        active_floor_num = switchableLayers[index].getProperties().floor_num;
        if (routeLayer) {
            var features = routeLayer.getSource().getFeatures();
            for (var i = 0; i < features.length; i++) {
                var feature_floor = features[i].getProperties().floor;
                if (feature_floor == active_floor_num) {
                    features[i].setStyle(route_active_style);
                } else {
                    features[i].setStyle(route_inactive_style);
                }
            }
        }
    }
    // if (floor_layers.length > 0) {
    //     floor_layers[index].setVisible(true);
    //     $("#floor-links li:nth-child(" + (floor_layers.length - index) + ")").addClass("active");
    //
    //     // set active_floor_num
    //     active_floor_num = floor_layers[index].getProperties().floor_num;
    //     if (routeLayer) {
    //         var features = routeLayer.getSource().getFeatures();
    //         for (var i = 0; i < features.length; i++) {
    //             var feature_floor = features[i].getProperties().floor;
    //             if (feature_floor == active_floor_num) {
    //                 features[i].setStyle(route_active_style);
    //             } else {
    //                 features[i].setStyle(route_inactive_style);
    //             }
    //         }
    //     }
    // }
}


function activateLayer(index) {
    hideLayers();
    setLayerVisible(index);
    update_url('map');
}