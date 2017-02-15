xStart = 1826602.5273166203;
yStart = 6142514.2285252055;


var view = new ol.View({
        center: [xStart, yStart],
        zoom: zoom_level
    });


var scaleLineControl = new ol.control.ScaleLine();
var map = new ol.Map({
    interactions: ol.interaction.defaults().extend([
        new ol.interaction.DragRotateAndZoom()
    ]),
    //layers: [backgroundLayers[0], backgroundLayers[1], wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03],
    layers: [backgroundLayerGroup, wmsfloorLayerGroup, poiLayerGroup
        // new ol.layer.Group({
        //     'title': gettext('Background'),
        //     layers: [grey_bmapat, ortho30cm_bmapat
        //     ]
        // }),
        // new ol.layer.Group({
        //     title: gettext('Floor'),
        //     layers: [
        //
        //         wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03, wmsE04, wmsE05, wmsE06
        //     ]
        // })
    ],
    target: 'map-block',
    controls: ol.control.defaults({
        attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
            collapsible: false
        })
    }).extend([ scaleLineControl]),
    view: view
});


// Change map height on resize
function fixContentHeight(){
    var viewHeight = $(window).height();
    var viewWidth = $(window).width();
    var $map_block = $("#map-block");
    if (viewWidth >= 990) {
        $map_block.height(viewHeight - 190);
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