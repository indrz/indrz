var baseApiUrl = '/indrz/api/v1/';
var baseApiRoutingUrl = '/indrz/api/v1/directions/';
var baseApiSearchUrl = baseApiUrl + 'search';
var baseUrlWms =  'http://gis-neu.wu.ac.at:8080/geoserver290/indrz/wms';
var zoom_level="{{ zoom_level }}";
var campus_id="{{ campus_id}}";
var floor = "{{ floor_num }}";
var building_id="{{ building_id }}";
var floor_id="{{ floor_id }}";
var floor_num = "{{ floor_num }}";
var space_id="{{ space_id }}";
var active_floor_num="{{ floor_num }}";
var floor_layers = [];
var timer_waitfor_floor = null;
var building_info = null;
var map_name="{{map_name}}";
var route_from = "{{route_from}}";
var route_to = "{{route_to}}";
var centerx = "{{centerx}}";
var centery = "{{centery}}";

var StartCenterX = 1826602.5273166203;
var StartCenterY = 6142514.2285252055;

