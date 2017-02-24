$(document).ready(function () {


    function loadShare(){
        if(search_text != '' && search_text.length > 0){
            searchIndrz(1, search_text)

        }

    }

    function initialize() {


        if (centerx != 0 && centery != 0 && isNaN(centerx) == false) {

                var view = map.getView();
                view.setCenter([centerx, centery]);
                view.setZoom(zoom_level);
            }

        // if(poi_id != 0){
        //     searchIndrz(1, search_string)
        //         // map.getLayers().push(spaceLayer);
        // }
        //
			if(document.location.href.split('?')[1] != null){
				if(document.location.href.split('?')[1].split("key=")[1] != null){
					var key = document.location.href.split('?')[1].split("key=")[1].split("&")[0];
					calculateLibraryRoute(key);
				}
			}


        if (floor_layers.length > 0) {

            if (route_from != '' && route_to != '') {

                initRoute(route_from, route_to);

                $("#route-from").val(route_from);
                $("#route-to").val(route_to);
                // $("#directionsForm").submit();
                $('#collapseTwo').collapse('show'); // open the accordian point routing
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
    loadShare();
    calculateLibraryRoute("ST 261.w34 G744");


});