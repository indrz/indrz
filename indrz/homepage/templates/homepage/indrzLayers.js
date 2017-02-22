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
        'https://maps1.wien.gv.at/basemap/' + templatepng,
        'https://maps2.wien.gv.at/basemap/' + templatepng,
        'https:///maps3.wien.gv.at/basemap/' + templatepng,
        'https://maps4.wien.gv.at/basemap/' + templatepng
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
        name: layerSrcName,
        source: WmtsTileSource,
        minResolution: 0.298582141738,
        visible: isVisible,
        type: "background"

    });

    return wmtsLayer;


}


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
        floor_num: floorNumber,
        type: "floor",
        zIndex: zIndexValue,
        crossOrigin: "anonymous"

    });

    return newWmsLayer;
}

var grey_bmapat = createWmtsLayer('bmapgrau', '.png', true);
var wmsOutdoorMap = createWmsLayer('outdoorMap', 'indrz:outdoor', '0', 'true', 1 );
var ortho30cm_bmapat = createWmtsLayer('bmaporthofoto30cm', '.jpg', false);

var backgroundLayerGroup = new ol.layer.Group({layers: [grey_bmapat, wmsOutdoorMap, ortho30cm_bmapat], name: gettext("background maps")});


var wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03, wmsE04, wmsE05, wmsE06;
wmsUG01 = createWmsLayer('ug01', 'indrz:ug01', '-1', 'false', 3);
wmsE00 = createWmsLayer('e00', 'indrz:e00', '0', 'true', 3);
wmsE01 = createWmsLayer('e01', 'indrz:e01', '1', 'false', 3);
wmsE02 = createWmsLayer('e02', 'indrz:e02', '2', 'false', 3);
wmsE03 = createWmsLayer('e03', 'indrz:e03', '3', 'false', 3);
wmsE04 = createWmsLayer('e04', 'indrz:e04', '4', 'false', 3 );
wmsE05 = createWmsLayer('e05', 'indrz:e05', '5', 'false', 3 );
wmsE06 = createWmsLayer('e06', 'indrz:e06', '6', 'false', 3 );


var wmsfloorLayerGroup = new ol.layer.Group({layers: [wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03, wmsE04, wmsE05, wmsE06], name: gettext("wms floor maps")});


var poiLayerGroup = new ol.layer.Group({layers: [], name: gettext("poi group")});

// var floor_layers = [ wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03, wmsE04, wmsE05, wmsE06 ];

var OsmBackLayer = new ol.layer.Tile({
    source: new ol.source.OSM(),
    visible: true,
    type: "background"
});


$.ajax( baseApiUrl + "campus/1/floors/" )
    .then(function (response) {
        floors_info = response;

        for (var i = 0; i < floors_info.length; ++i) {
            floor_layers.push(floors_info[i]);
            appendFloorNav(floors_info[i].short_name, [i]);
            }

        activateLayer(floor_num);

    });


function appendFloorNav(floor_info, index) {
    $("#floor-links").prepend("<li class='list-group-item' >" +
        "<a href='#' onclick='activateLayer(" + index + ");' id='floorIndex_" + index  + "' class='indrz-floorswitcher' >" + floor_info + " </a>" +
        "</li>");
    // Add flour to mobile ui element
    $("#floor-links-select").prepend("<option value='" + index + "'>" + floor_info + "</option>");
}
