var routeLocalDataKiosk = {};
// passing in `null` for the `options` arguments will result in the default
// options being used
$('#search-input-kiosk').typeahead(null, {
    hint: true,
    highlight: true,
    minLength: 1,
    name: 'search-field',
    limit: 100,
    source: searchValues
    // templates: {
    //         empty: 'not found', //optional
    //         suggestion: function(el){return '<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREZsX_jcmMUqvVF3HW8-3dyjxZ9wZO4ugIvYQyj761-RYwcH91" />'+el.name}
    //     }


});

$('#search-input-kiosk').on('typeahead:selected', function (e, item) {
    console.log("selected item: " + item);
    searchIndrzKiosk(building_id, item);


}).on('typeahead:autocompleted', function (e, item) {
    console.log("autocompleted item: " + item);
});



    // var endSearchText = $('#route-to').val();
    // var routeType = $("input:radio[name=typeRoute]:checked").val();
    //
    //
    //     $.when(fetcherMd(endSearchText)).then(function(b) {
    //
    //     routeLocalDataKiosk.end = {};
    //     routeLocalDataKiosk.end.xcoord = b[0].features[0].properties.centerGeometry.coordinates[0];
    //     routeLocalDataKiosk.end.ycoord = b[0].features[0].properties.centerGeometry.coordinates[1];
    //     routeLocalDataKiosk.end.floor = b[0].features[0].properties.floor_num;
    //     var routeEndValue = routeLocalDataKiosk.end.xcoord + "," + routeLocalDataKiosk.end.ycoord + "," + routeLocalDataKiosk.end.floor;
    //
    //     routeLocalDataKiosk.end.routeValue = routeEndValue;
    //
    //
    //     console.log(b[0]);
    //
    //     console.log(JSON.stringify(routeLocalDataKiosk));
    //
    //     console.log("END IS "+b[0].features[0].properties);
    //
    //     getDirectionsFromKiosk(routeEndValue,0);
    //
    // });




