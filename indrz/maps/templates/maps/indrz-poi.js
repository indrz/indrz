var poiUrl = {{ poi_url }};
var poiUrl = 'http://openlayers.org/en/v3.17.1/examples/data/icon.png';

var indrzIconFeature = new ol.Feature({
    geometry: new ol.geom.Point([0, 0]),
    name: {{ poi_name }},
    category: {{ poi_categrory }},
    rainfall: 500
})

var iconStyle = new ol.style.Style({
    image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
        anchor: [0.5, 46],
        anchorXUnits: 'fraction',
        anchorYUnits: 'pixels',
        src: poiUrl
    }))
});

indrzIconFeature.setStyle(iconStyle);

var poiVectorSource = new ol.source.Vector({
    features: [indrzIconFeature]
});

var poiVectorLayer = new ol.layer.Vector({
    source: poiVectorSource
});

