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


var building_id = 1;

var searchValues = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    // prefetch: baseApiUrl + 'spaces/search/?format=json',
    prefetch: '/autocomplete/%QUERY?.format=json',
    remote: {
      url: '/autocomplete/%QUERY?.format=json',
      wildcard: '%QUERY'
    }
});

// passing in `null` for the `options` arguments will result in the default
// options being used
$('#search-input').typeahead(null, {
    hint: true,
    highlight: true,
    minLength: 1,
    name: 'search-field',
    limit: 100,
    source: searchValues
});


$("#submitFormSearch").submit(function (event) {
    //              alert( "Handler for .submit() called."  );

    //            var buildingid = buildingNantesId;
    var searchText = $('#search-input').val();
    searchIndrz(building_id, searchText);
    event.preventDefault();
});

$("#showPoi").submit(function (event) {
   // alert( "Handler for .submit() called." + $('#poi-input').val()   );
    var poiName = $('#poi-input').val();
    searchPoi(building_id, poiName);
    event.preventDefault();
    });

       var roomNums = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: baseApiUrl + 'spaces/search/?format=json'
});
// passing in `null` for the `options` arguments will result in the default
// options being used
$('#rooms-prefetch .typeahead').typeahead(null, {
    name: 'countries',
    limit: 100,
    source: roomNums
});
$("#submitForm").submit(function (event) {
    // alert( "Handler for .submit() called."  );
    var startNum = $('#route-from').val();
    var endNum = $('#route-to').val();
    var rType = $("input:radio[name=typeRoute]:checked").val();
    addRoute(startNum, endNum, rType);
    event.preventDefault();
});

