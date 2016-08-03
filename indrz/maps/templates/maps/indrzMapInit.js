
var view = new ol.View({
        center: [StartCenterX, StartCenterY],
        zoom: zoom_level
    });

var map = new ol.Map({
    interactions: ol.interaction.defaults().extend([
        new ol.interaction.DragRotateAndZoom()
    ]),
    //layers: [backgroundLayers[0], backgroundLayers[1], wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03],
    layers: [
        new ol.layer.Group({
            'title': gettext('Background'),
            layers: [OsmBackLayer
            ]
        }),
        new ol.layer.Group({
            title: gettext('Floor'),
            layers: [

                wmsUG01, wmsE00, wmsE01, wmsE02, wmsE03 //, wmsE04, wmsE05, wmsE06
            ]
        })
    ],
    target: 'map-block',
    controls: ol.control.defaults({
        attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
            collapsible: false
        })
    }),
    view: view
});

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