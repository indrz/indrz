var capabilitiesUrl = 'http://www.basemap.at/wmts/1.0.0/WMTSCapabilities.xml';
var IS_CROSS_ORIGIN = 'anonymous';

    var templatepng =
        '{Layer}/{Style}/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}.png';

    var urlsbmappng = [
        '//maps1.wien.gv.at/basemap/' + templatepng,
        '//maps2.wien.gv.at/basemap/' + templatepng,
        '//maps3.wien.gv.at/basemap/' + templatepng,
        '//maps4.wien.gv.at/basemap/' + templatepng
    ];

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

    // Grau
    var bmapgrau = new ol.source.WMTS({
        tilePixelRatio: 1,
        projection: ol.proj.get('EPSG:3857'),
        layer: 'bmapgrau',
        style: 'normal',
        matrixSet: 'google3857',
        urls: urlsbmappng,
        crossOrigin: IS_CROSS_ORIGIN,
        requestEncoding: /** @type {ol.source.WMTSRequestEncoding} */ ('REST'),
        tileGrid: tilegrid,
        attributions: [
            new ol.Attribution({
                html: 'Tiles &copy; <a href="//www.basemap.at/">' +
                    'basemap.at</a> (GRAU).'
            })
        ]
    });

    var bmapgrauLayer = new ol.layer.Tile({
        name: 'basemap.at - GRAU',
        source: bmapgrau,
        minResolution: 0.298582141738,
        isBaseLayer: true,
        visible: false
    });


var map = new ol.Map({
    interactions: ol.interaction.defaults().extend([
        new ol.interaction.DragRotateAndZoom()
    ]),
    //layers: [backgroundLayers[0], backgroundLayers[1], wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03],
    layers: [
        new ol.layer.Group({
            'title': 'Background',
            layers: [bmapgrauLayer
            ]
        }),
        new ol.layer.Group({
            title: 'Ebene',
            layers: [

                wmsUG01, wmsEG00, wmsEG01, wmsEG02, wmsEG03, wmsEG04, wmsEG05, wmsEG06
            ]
        })
    ],
    target: 'map-block',
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

// $.ajax(capabilitiesUrl).then(function(response) {
//   var result = new ol.format.WMTSCapabilities().read(response);
//   var options = ol.source.WMTS.optionsFromCapabilities(result, {
//     layer: layer,
//     matrixSet: 'google3857',
//     requestEncoding: 'REST',
//     style: 'normal'
//   });
//   options.tilePixelRatio = tilePixelRatio;
//   map.addLayer(new ol.layer.Tile({
//     source: new ol.source.WMTS(options)
//   }));
// });


// Change map height on resize
function fixContentHeight(){
    var viewHeight = $(window).height();
    var viewWidth = $(window).width();
    var $map_block = $("#map-block");
    if (viewWidth >= 990) {
        $map_block.height(viewHeight);
    } else {
        var navbar = $(".navbar:visible:visible");
        var contentHeight = viewHeight - navbar.outerHeight();
        $map_block.height(contentHeight);
    }
    map.updateSize();
}

$(window).resize(function () {
    fixContentHeight();
});

$(document).ready(function () {
    fixContentHeight();

});
