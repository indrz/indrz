var map_type = true;

var full_screen_control = new ol.control.FullScreen({
    label: "Go Full Screen",
    className: "btn-fullscreen",
    target: document.getElementById("id-fullscreen")
});

// map.addControl(full_screen_control);

$("#id-map-switcher").on("click", function(evt){
    map_type = !map_type;
    if(map_type) {
        $(this).text('Satellite');
        ortho30cm_bmapat.setVisible(false);
        grey_bmapat.setVisible(true);
        wmsOutdoorMap.setVisible(true);

        setLayerVisible(1);

    } else {
        $(this).text('Map');
        ortho30cm_bmapat.setVisible(true);
        grey_bmapat.setVisible(false);
        wmsOutdoorMap.setVisible(false);
        hideLayers();
    }
});


var panToCampus = document.getElementById('id-zoom-to-campus');

panToCampus.addEventListener('click', function() {
    var pan = ol.animation.pan({
      duration: 2000,
      source: /** @type {ol.Coordinate} */ (view.getCenter())
    });
    map.beforeRender(pan);
    view.setCenter(CampusZoom);
    view.setZoom(17);
    }, false);


