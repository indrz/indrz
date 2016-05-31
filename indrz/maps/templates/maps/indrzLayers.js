function createWmsLayer(layerName, geoserverLayer, floorNumber, isVisible, zIndexValue){
    var newWmsLayer = new ol.layer.Image({
    source: new ol.source.ImageWMS({
        url: baseUrlWms,
        params: {'LAYERS': geoserverLayer},
        serverType: 'geoserver',
        crossOrigin: ''
    }),
    visible: isVisible,
    name: layerName,
    floor: floorNumber,
    type: "floor",
    zIndex: zIndexValue

});

    return newWmsLayer;
}


wmsUG01 = createWmsLayer('wmsUG01','indrz:ug01', '-1', 'false', 3 );
wmsE00 = createWmsLayer('wmsE00','indrz:e00', '0', 'false', 3 );
wmsE01 = createWmsLayer('wmsE01','indrz:e01', '1', 'false', 3 );
wmsE02 = createWmsLayer('wmsE02','indrz:e02', '2', 'false', 3 );
wmsE03 = createWmsLayer('wmsE03','indrz:e03', '3', 'false', 3 );
// wmsE04 = createWmsLayer('wmsE04','indrz:e04', '4', 'false', 3 );
// wmsE05 = createWmsLayer('wmsE05','indrz:e05', '5', 'false', 3 );
// wmsE06 = createWmsLayer('wmsE06','indrz:e06', '6', 'false', 3 );

var mapQuestOsm = new ol.layer.Tile({
    source: new ol.source.MapQuest({
        layer: 'osm'}),
    visible: false,
    type: "background"});

var OsmBackLayer = new ol.layer.Tile({
    source: new ol.source.OSM(),
    visible: true,
    type:"background"});

var SatelliteLayer = new ol.layer.Tile({
    source: new ol.source.MapQuest({layer: 'sat'}),
    visible: false,
    type:"background"});

$.ajax('/api/v1/buildings/' + building_id +'/')
    .then(function(response) {
        building_info = response;
        for(var i=0; i< response.num_floors; i++){
            var geojsonFormat = new ol.format.GeoJSON();
            var floor_info = response.buildingfloor_set[i];
            var features = geojsonFormat.readFeatures(floor_info.buildingfloorspace_set,
                {featureProjection: 'EPSG:4326'});
            var spaces_source =  new ol.source.Vector();
            spaces_source.addFeatures(features);

            var floor_spaces_vector = new ol.layer.Vector({
                source: spaces_source,
                style:  new ol.style.Style({
                    fill: new ol.style.Fill({
                        color: 'rgba(255, 255, 255, 0.6)'
                    }),
                    stroke: new ol.style.Stroke({
                      color: 'grey',
                      width: 1
                    })
                  }),
                title: "spaces",
                name: "spaces",
                floor_num: floor_info.floor_num,
                visible: false,
                zIndex: 99
            });
            map.getLayers().push(floor_spaces_vector);
            floor_layers.push(floor_spaces_vector);
            appendFloorNav(floor_info, i);
        }
        if(space_id=="0"){
            for(var i=0; i< floor_layers.length; i++) {
                if(active_floor_num == floor_layers[i].getProperties().floor_num){
                    activateLayer(i);
                }
            }
        }
});


function appendFloorNav(floor_info, index){
    $("#floor-links").prepend("<li>" +
    "<a href='#' onclick='activateLayer(" +
    index +
    ");' id='action-1'>"+ floor_info.short_name +"</a></li>");
}
