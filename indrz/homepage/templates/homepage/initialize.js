$(document).ready(function () {
    function initialize() {


        if (centerx != 0 && centery != 0 && isNaN(centerx) == false) {

                var view = map.getView();
                view.setCenter([centerx, centery]);
                view.setZoom(zoom_level);
            }

        if (floor_layers.length > 0) {

            if (route_from != '' && route_to != '') {
                $("#route-from").val(route_from);
                $("#route-to").val(route_to);
                $("#submitForm").submit();
            } else if (centerx != 0 && centery != 0 && isNaN(centerx) == false) {
                var view = map.getView();
                view.setCenter([centerx, centery]);
                view.setZoom(zoom_level);
            }
        } else {
            setTimeout(initialize, 250);
        }
    }

    initialize();
});