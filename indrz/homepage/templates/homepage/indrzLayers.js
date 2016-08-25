var tilegrid = new ol.tilegrid.WMTS({
    origin: [-20037508.3428, 20037508.3428],
    extent: [977650, 5838030, 1913530, 6281290],
    resolutions: [
        156543.03392811998,
        78271.51696419998,
        39135.758481959994,
        19567.879241008,
        9783.939620504,
        4891.969810252,
        2445.984905126,
        1222.9924525644,
        611.4962262807999,
        305.74811314039994,
        152.87405657047998,
        76.43702828523999,
        38.21851414248,
        19.109257071295996,
        9.554628535647998,
        4.777314267823999,
        2.3886571339119995,
        1.1943285669559998,
        0.5971642834779999,
        0.29858214174039993,
        0.14929107086936
    ],
    ////resolutions: [
    ////    559082264.029 * 0.28E-3,
    ////    279541132.015 * 0.28E-3,
    ////    139770566.007 * 0.28E-3,
    ////    69885283.0036 * 0.28E-3,
    ////    34942641.5018 * 0.28E-3,
    ////    17471320.7509 * 0.28E-3,
    ////    8735660.37545 * 0.28E-3,
    ////    4367830.18773 * 0.28E-3,
    ////    2183915.09386 * 0.28E-3,
    ////    1091957.54693 * 0.28E-3,
    ////    545978.773466 * 0.28E-3,
    ////    272989.386733 * 0.28E-3,
    ////    136494.693366 * 0.28E-3,
    ////    68247.3466832 * 0.28E-3,
    ////    34123.6733416 * 0.28E-3,
    ////    17061.8366708 * 0.28E-3,
    ////    8530.91833540 * 0.28E-3,
    ////    4265.45916770 * 0.28E-3,
    ////    2132.72958385 * 0.28E-3,
    ////    1066.36479193 * 0.28E-3,
    ////    533.182395962 * 0.28E-3
    ////],
    matrixIds: [
        '0',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '10',
        '11',
        '12',
        '13',
        '14',
        '15',
        '16',
        '17',
        '18',
        '19',
        '20'
    ]
});



function createWmtsLayer(layerSrcName, type, isVisible) {
    var gg, sm, templatepng, urlsbmappng, WmtsTileSource, wmtsLayer;
    gg = ol.proj.get('EPSG:4326');
    sm = ol.proj.get('EPSG:3857');
    templatepng = '{Layer}/{Style}/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}' + type;
    urlsbmappng = [
        'http://maps1.wien.gv.at/basemap/' + templatepng,
        'http://maps2.wien.gv.at/basemap/' + templatepng,
        'http:///maps3.wien.gv.at/basemap/' + templatepng,
        'http://maps4.wien.gv.at/basemap/' + templatepng
    ];


    WmtsTileSource = new ol.source.WMTS({
        tilePixelRatio: 1,
        projection: sm,
        layer: layerSrcName,
        style: 'normal',
        matrixSet: 'google3857',
        urls: urlsbmappng,
        crossOrigin: 'anonymous',
        requestEncoding: /** @type {ol.source.WMTSRequestEncoding} */ ('REST'),
        tileGrid: tilegrid,
        attributions: [
            new ol.Attribution({
                html: 'Tiles &copy; <a href="//www.basemap.at/">basemap.at</a>'
            })
        ]
    });

    wmtsLayer = new ol.layer.Tile({
        name: 'basemap.at - GRAU',
        source: WmtsTileSource,
        minResolution: 0.298582141738,
        visible: isVisible,
        type: "background"

    });

    return wmtsLayer;


}


var grey_bmapat = createWmtsLayer('bmapgrau', '.png', true);
var ortho30cm_bmapat = createWmtsLayer('bmaporthofoto30cm', '.jpg', false);


function createWmsLayer(layerName, geoserverLayer, floorNumber, isVisible, zIndexValue) {
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
        zIndex: zIndexValue,
        crossOrigin: "anonymous"

    });

    return newWmsLayer;
}

var wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03, wmsE04, wmsE05, wmsE06;
wmsUG01 = createWmsLayer('ug01', 'indrz:ug01', '-1', 'false', 3);
wmsE00 = createWmsLayer('eg00', 'indrz:e00', '0', 'true', 3);
wmsE01 = createWmsLayer('og01', 'indrz:e01', '1', 'false', 3);
wmsE02 = createWmsLayer('og02', 'indrz:e02', '2', 'false', 3);
wmsE03 = createWmsLayer('og03', 'indrz:e03', '3', 'false', 3);
wmsE04 = createWmsLayer('og04', 'indrz:e04', '4', 'false', 3 );
wmsE05 = createWmsLayer('og05', 'indrz:e05', '5', 'false', 3 );
wmsE06 = createWmsLayer('og06', 'indrz:e06', '6', 'false', 3 );

// var floor_layers = [ wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03, wmsE04, wmsE05, wmsE06 ];

var OsmBackLayer = new ol.layer.Tile({
    source: new ol.source.OSM(),
    visible: true,
    type: "background"
});

// gets all spaces on a single floor for all buildings on campus
$.ajax('/api/v1/buildings/' + building_id + '/')
    .then(function (response) {
        building_info = response;
        for (var i = 0; i < response.num_floors; i++) {
            var geojsonFormat = new ol.format.GeoJSON();
            var floor_info = response.buildingfloor_set[i];
            var features = geojsonFormat.readFeatures(floor_info.buildingfloorspace_set,
                {featureProjection: 'EPSG:4326'});
            var spaces_source = new ol.source.Vector();
            spaces_source.addFeatures(features);

            var floor_spaces_vector = new ol.layer.Vector({
                source: spaces_source,
                style: new ol.style.Style({
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
        if (space_id == "0") {
            for (var i = 0; i < floor_layers.length; i++) {
                if (active_floor_num == floor_layers[i].getProperties().floor_num) {
                    activateLayer(i);
                }
            }
        }
    });


function appendFloorNav(floor_info, index) {
    $("#floor-links").prepend("<li>" +
        "<a href='#' onclick='activateLayer(" +
        index +
        ");' id='action-1'>" + floor_info.short_name + "</a></li>");
    // Add flour to mobile ui element
    $("#floor-links-select").prepend("<option value='" + index + "'>" + floor_info.short_name + "</option>");
}
