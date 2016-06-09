
var baseUrlWms =  'http://137.208.3.187:8080/geoserver/wuwien/wms';
var zoom_level="{{ zoom_level }}";
var building_id="{{ building_id }}";
var active_floor_num="{{floor_num}}";
var space_id="{{ space_id }}";
var floor_layers = [];
var timer_waitfor_floor = null;
var building_info = null;
var map_name="{{map_name}}";
var route_from = "{{route_from}}";
var route_to = "{{route_to}}";
var centerx = "{{centerx}}";
var centery = "{{centery}}";

var wms_floor_names= ["wmsUG01", "wmsEG00", "wmsEG01", "wmsEG02", "wmsEG03", "wmsEG04", "wmsEG05", "wmsEG06"];

var StartCenterX = 1826602.5273166203;
var StartCenterY = 6142514.2285252055;
// set the starting coordinate of the map
