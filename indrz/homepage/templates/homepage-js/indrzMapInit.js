var map = new ol.Map({
    interactions: ol.interaction.defaults().extend([
        new ol.interaction.DragRotateAndZoom()
    ]),
    //layers: [backgroundLayers[0], backgroundLayers[1], wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03],
    layers: [
        new ol.layer.Group({
            'title': 'Background',
            layers: [mapQuestOsm, OsmBackLayer, SatelliteLayer
            ]
        }),
        new ol.layer.Group({
            title: 'Ebene',
            layers: [

                wmsUG01, wmsEG00, wmsEG01, wmsEG02, wmsEG03, wmsEG04, wmsEG05, wmsEG06
            ]
        })
    ],
    target: 'map',
    controls: ol.control.defaults({
        attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
            collapsible: false
        })
    }),
    view: new ol.View({
        center: [StartCenterX, StartCenterY],
        zoom: zoom_level
    })
});

