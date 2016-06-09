var style = new ol.style.Style({
  fill: new ol.style.Fill({
    color: 'rgba(255, 255, 255, 0.6)'
  }),
  stroke: new ol.style.Stroke({
    color: '#319FD3',
    width: 2
  }),
  text: new ol.style.Text({
    font: 'bold 12px Arial,sans-serif',
    fill: new ol.style.Fill({
      color: '#000'
    }),
      maxResolution : 2000,
    stroke: new ol.style.Stroke({
      color: '#fff',
      width: 3
    })
  })
});

var styles = [style];
  var getText = function(feature, resolution) {

      if (feature ) {

          if (feature.get('short_name') !== null)
          {
              //info.innerHTML = feature.getId() + ': ' + feature.get('name');
              style.getText().setText(resolution < 0.1 ? feature.get('short_name') : '');
                return styles;

              }
          }
    };

var spaceJSONURL = '/api/v1/buildings/space/'+ space_id +'.json';

var space_source = new ol.source.Vector();
$.ajax(spaceJSONURL).then(function(response) {
    var geojsonFormat = new ol.format.GeoJSON();
    var features = geojsonFormat.readFeatures(response,
        {featureProjection: 'EPSG:4326'});
    space_source.addFeatures(features);
    var space_floor_id = features[0].getProperties().fk_building_floor.id;
    waitForFloors(space_floor_id);

    var center_crd = ol.extent.getCenter(space_source.getExtent());
    open_popup(features[0].getProperties(), center_crd);

    // zoom to the room
    map.getView().fit(space_source.getExtent(), map.getSize());
});


var spaceLayer = new ol.layer.Vector({
    source: space_source,
    style: getText,
    title: "Space",
    name: "Space",
    zIndex: 999
});

map.getLayers().push(spaceLayer);