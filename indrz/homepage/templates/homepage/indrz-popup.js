{% load i18n %}
var popup_container = document.getElementById('indrz-popup');
var popup_content = document.getElementById('popup-content');
var popup_links = document.getElementById('popup-links');
var popup_closer = document.getElementById('popup-closer');


var selectRoom = new ol.interaction.Select();

/**
 * Create an overlay to anchor the popup to the map.
 */
var popup_overlay = new ol.Overlay(/** @type {olx.OverlayOptions} */ ({
  element: popup_container,
  autoPan: true,
  autoPanAnimation: {
    duration: 250
  },
  zIndex: 99
}));

/**
 * Add a click handler to hide the popup.
 * @return {boolean} Don't follow the href.
 */
function close_popup(){
  popup_overlay.setPosition(undefined);
  popup_closer.blur();
    // if (searchLayer) {
    //     map.removeLayer(searchLayer);
    //
    // }
  return false;
}

popup_closer.onclick = function() {
  popup_overlay.setPosition(undefined);
  popup_closer.blur();
    // if (searchLayer) {
    //     map.removeLayer(searchLayer);
    //     //map.getLayers().pop();
    // }
    // map.getLayers().pop();
  return false;
};



map.addOverlay(popup_overlay);

map.addInteraction(selectRoom);

map.on('singleclick', function (e) {
  map.forEachFeatureAtPixel(e.pixel, function (feature, layer) {

      if(feature.getGeometry().getType() == "MultiPolygon" || feature.getGeometry().getType() == "MultiPoint") {
          var coordinate = map.getCoordinateFromPixel(e.pixel);
          var properties = feature.getProperties();
          open_popup(properties, coordinate);
          console.log("inside popup click action")
      }
  });
});

function getTitle(properties){
    var name;
    if (properties.label) {
        name = properties.label;
        return name;
    }
    else if(properties.short_name){
        name = properties.short_name;
        return name;
    }
    else if (properties.room_code){
        name = properties.room_code;
        return name;
    }
    else if (properties.fancyname_de){
        name = properties.fancyname_de;
        return name;
    }
    else if (properties.roomcode && properties.label != undefined){
        name = properties.roomcode;
        return name;

    }
    else if (properties.name) {
        name = properties.name;
        return name;
    }


}

var routeToValTemp = ""
var routeFromValTemp = ""

function open_popup(properties, coordinate, name){
    console.log("properites: " + properties.name)
    var titlePopup = ""
    var titleBuildingName = gettext('Building : ');
    var titleFloorNumber = gettext('Floor Number: ');
    var titleRoomcode = gettext('Room Number: ');
    //var name;
    var floorNum;
    var buildingName;
    var roomcode ;

    var name = "";

    titlePopup = getTitle(properties);

    routeToValTemp = titlePopup;
    routeFromValTemp = titlePopup;

    var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
      coordinate, 'EPSG:3857', 'EPSG:4326'));

    if (properties.label){
        //var properties = properties[0].properties;

        popupTitle = properties.label;
        floorNum = properties.floor_num;
        buildingName = properties.building_name;
        roomcode = properties.roomcode;
    } else {
        name = properties.roomcode;
        floorNum = properties.floor_num;
        buildingName = properties.building_name;
        roomcode = properties.roomcode;
    }


    popup_content.innerHTML = '<h4>' + titlePopup + '</h4>';
    popup_content.innerHTML += '<p>' + titleFloorNumber + floorNum + '</p>';

    if(properties.building_name != undefined || properties.building_name === ""){
        popup_content.innerHTML += '<p>' + titleBuildingName + buildingName + '</p>';
    }

    if(properties.roomcode != undefined){
        popup_content.innerHTML += '<p>' + titleRoomcode + roomcode + '</p>';
    }


    // uncomment below to show the coordinate in popup
    // popup_content.innerHTML += '<p>' + gettext('Coordinate: ')+ '</p><code>' + coordinate + '</code><p></p><code>' + hdms + '</code>';

    popup_overlay.setPosition(coordinate);
}

function close_popup(){
  popup_overlay.setPosition(undefined);
  popup_closer.blur();
    $("#search-input").val('');
  return false;
}


$(function() {
    $("#routeFromHere").click(function() {

        $('#collapseTwo').collapse('show');


            document.getElementById('route-from').value = routeFromValTemp;

        }
        )
});

$(function() {
    $("#routeToHere").click(function(){
        document.getElementById('route-to').value = routeToValTemp;
        $('#collapseTwo').collapse('show');

    }
        )
});

$(function() {
    $("#shareSearchPopup").click(function(){

        $('#ShareSearchModal').modal('show');


    }
        )
});



