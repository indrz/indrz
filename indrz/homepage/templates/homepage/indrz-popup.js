var popup_container = document.getElementById('indrz-popup');
var popup_content = document.getElementById('popup-content');
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
    if (searchLayer) {
        map.removeLayer(searchLayer);

    }
  return false;
}

popup_closer.onclick = function() {
  popup_overlay.setPosition(undefined);
  popup_closer.blur();
    if (searchLayer) {
        map.removeLayer(searchLayer);
        //map.getLayers().pop();
    }
    // map.getLayers().pop();
  return false;
};



map.addOverlay(popup_overlay);

map.addInteraction(selectRoom);

map.on('singleclick', function (e) {
  map.forEachFeatureAtPixel(e.pixel, function (feature, layer) {
      if(feature.getGeometry().getType() == "MultiPolygon") {
          var coordinate = map.getCoordinateFromPixel(e.pixel);
          var properties = feature.getProperties();
          open_popup(properties, coordinate);
      }
  });
});

function open_popup(properties, coordinate){

  var titlePopup = gettext('Building Name: ');

  var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
      coordinate, 'EPSG:3857', 'EPSG:4326'));
    if (properties.short_name){
        var name = properties.short_name;
        var floorNum = properties.floor_num;
        var buildingName = properties.building_name;
    } else {
        var name = properties.name;
        var floorNum = "0";
        var buildingName = properties.campus_name;
        titlePopup = gettext('Campus ');
    }

    var textFloorNumber = gettext('Floor Number: ');

    popup_content.innerHTML = '<h4>' + name + '</h4>';
    popup_content.innerHTML += '<p>' + textFloorNumber + floorNum + '</p>';
    popup_content.innerHTML += '<p>' + titlePopup + buildingName + '</p>';

  popup_content.innerHTML += '<p>' + gettext('Coordinate: ')+ '</p><code>' + hdms + '</code><p><a href="#"><i class="fa fa-bug fa-fw"></i>' + gettext('Bug Report') + '</a>  </p>';
  popup_overlay.setPosition(coordinate);
}

function close_popup(){
  popup_overlay.setPosition(undefined);
  popup_closer.blur();
    $("#search-input").val('');
  return false;
}
/*
map.on('singleclick', function(evt) {
  var coordinate = evt.coordinate;
  var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
        coordinate, 'EPSG:3857', 'EPSG:4326'));

  popup_content.innerHTML = '<p>Coordinate:</p><code>' + hdms + '</code><p><a href="#"><i class="fa fa-bug fa-fw"></i> Bug report</a>  </p>';
  popup_overlay.setPosition(coordinate)
});

*/