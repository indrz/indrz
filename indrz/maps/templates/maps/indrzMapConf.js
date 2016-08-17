var baseUrlWms = '';
var zoom_level = "{{ zoom_level }}";
var campus_id = "{{ campus_id}}";
var building_id = "{{ building_id }}";
var floor_id = "{{ floor_id }}";
var space_id = "{{ space_id }}";
var active_floor_num = "{{floor_num}}";
var floor_layers = [];
var timer_waitfor_floor = null;
var building_info = null;
var map_name = "{{map_name}}";
var route_from = "{{route_from}}";
var route_to = "{{route_to}}";
var centerx = "{{centerx}}";
var centery = "{{centery}}";

var StartCenterX = -168547.958404064;
var StartCenterY = 5983885.94934575;
// set the starting coordinate of the map
