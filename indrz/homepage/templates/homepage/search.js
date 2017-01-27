var searchLayer = null;


var image = new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
            anchor: [0.5, 46],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: '/static/homepage/img/access_parking_p1.png'
        }));


var styles = {
  'Point': [new ol.style.Style({
    image: image
  })],
  'LineString': [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: 'green',
      width: 1
    })
  })],
  'MultiLineString': [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: 'green',
      width: 1
    })
  })],
  'MultiPoint': [new ol.style.Style({
    image: image
  })],
  'MultiPolygon': [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: '#21B6D8',
      width: 3
    }),
    fill: new ol.style.Fill({
      color: 'rgba(38, 215, 255, 0.2)'
    })
  })],
  'Polygon': [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: 'blue',
      lineDash: [4],
      width: 3
    }),
    fill: new ol.style.Fill({
      color: 'rgba(0, 0, 255, 0.1)'
    })
  })],
  'GeometryCollection': [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: 'magenta',
      width: 2
    }),
    fill: new ol.style.Fill({
      color: 'magenta'
    }),
    image: new ol.style.Circle({
      radius: 10,
      fill: null,
      stroke: new ol.style.Stroke({
        color: 'magenta'
      })
    })
  })],
  'Circle': [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: 'red',
      width: 2
    }),
    fill: new ol.style.Fill({
      color: 'rgba(255,0,0,0.2)'
    })
  })]
};

var styleFunction = function(feature, resolution) {
  return styles[feature.getGeometry().getType()];
};


var search_res_style = new ol.style.Style({
    fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 0.6)'
    }),
    stroke: new ol.style.Stroke({
        color: '#319FD3',
        width: 2
    }),
    text: new ol.style.Text({
        font: 'bold 12px Arial,sans-serif',
        fill: new ol.style.Fill({
            color: '#000'
        }),
        maxResolution: 2000,
        stroke: new ol.style.Stroke({
            color: '#fff',
            width: 3
        })
    })
});


function setSearchFeatureStyle(feature, resolution) {
    if (feature) {

        if (feature.get('short_name') !== null) {
            //info.innerHTML = feature.getId() + ': ' + feature.get('name');
            search_res_style.getText().setText(resolution < 0.1 ? feature.get('short_name') : '');
            return [search_res_style];

        }
    }

}

function zoomToFeature(source) {

    var view = map.getView();
    // // view.setCenter([centerx, centery]);
    // view.setZoom(19);

    var feature = source.getFeatures()[0];
    var polygon = /** @type {ol.geom.SimpleGeometry} */ (feature.getGeometry());
    var size = /** @type {ol.Size} */ (map.getSize());
    view.fit(polygon, size, {padding: [170, 50, 30, 150], constrainResolution: false})

    // view.fit(polygon, size, {padding: [170, 50, 30, 150], nearest: true})}
    // view.fit(point, size, {padding: [170, 50, 30, 150], minResolution: 50})}
    }


function zoomer(coord, zoom){
        var pan = ol.animation.pan({
          duration: 2000,
          source: /** @type {ol.Coordinate} */ (view.getCenter())
        });
        map.beforeRender(pan);

        view.setCenter(coord);
       // view.setZoom(zoom)
    }


function activateFloor(feature){
    // feature.get('floor_num')
    var searchResFloorNum = feature.getProperties().floor_num;
    for (var i = 0; i < switchableLayers.length; i++) {
        if (searchResFloorNum == switchableLayers[i].getProperties().floor_num) {
            activateLayer(i);
        }
    }

}

function clearSearchResults(){
            close_popup();

            $("#search-results-list").empty()
            $("#search-res").addClass("hide");
            $("#clearSearch").addClass("hide");
            $("#shareSearch").addClass("hide");
            $("#search-input").val('');

}


function searchIndrz(campusId, searchString) {
    // var searchUrl = '/api/v1/buildings/' + buildingId + '/' + spaceName + '.json';
    // var searchUrl = baseApiUrl + 'campus/' + campusId + '/search/' + searchString + '?format=json';
    var searchUrl = '/search/' + searchString + '?format=json';

    if (searchLayer) {
        map.removeLayer(searchLayer);
        clearSearchResults();

    }



    var searchSource = new ol.source.Vector();
    $.ajax(searchUrl).then(function (response) {
        var geojsonFormat3 = new ol.format.GeoJSON();
        var featuresSearch = geojsonFormat3.readFeatures(response,
            {featureProjection: 'EPSG:4326'});
        searchSource.addFeatures(featuresSearch);

        searchSource.forEachFeature(function(feature) {

            var att = feature.get("name");
            var floor = feature.get("floor_num");
            var roomcat = feature.get('category_de');
            var infoo = '"' + att + '"'
            if (roomcat != "" && roomcat != undefined){
                var htmlInsert = "<a href='#' onclick='showRes(" + infoo + ")' id='searchResListItem_"+ att +
                "' class='list-group-item indrz-search-res' >" + att +" ("+ roomcat + ") <span class='badge'>"+ gettext('Floor  ') + floor +"</span> </a>"
            }
            else{
                 var htmlInsert = "<a href='#' onclick='showRes(" + infoo + ")' id='searchResListItem_"+ att +
                "' class='list-group-item indrz-search-res' >" + att + " <span class='badge'>"+ gettext('Floor  ') + floor +"</span> </a>"
            }




            $("#search-results-list").append(htmlInsert);
            });


        var centerCoord = ol.extent.getCenter(searchSource.getExtent());

        if (featuresSearch.length === 1){

            open_popup(featuresSearch[0].getProperties(), centerCoord);

        }

        space_id = response.features[0].properties.space_id;
        poi_id = response.features[0].properties.poi_id;
        search_text = searchString;

        // active the floor of the start point
        activateFloor(featuresSearch[0]);

    } );


    searchLayer = new ol.layer.Vector({
        source: searchSource,
        style: styleFunction,
        title: "SearchLayer",
        name: "SearchLayer",
        zIndex: 999
    });

    map.getLayers().push(searchLayer);

    $("#search-res").removeClass("hide");
    $("#clearSearch").removeClass("hide");
    $("#shareSearch").removeClass("hide");

}


$("#clearSearch").click(function () {
    if (searchLayer) {
        map.removeLayer(searchLayer);
    }

    clearSearchResults();

});


function showRes(featureName){
    searchLayer.getSource().forEachFeature(function(feature) {
        if (feature.get('name') === featureName ){
            open_popup(feature.getProperties(), feature.get('centerGeometry').coordinates);

            activateFloor(feature);

        }

    })


}

// function getResultFromURLWithCallback(url, callback)
// {
//
// 	return $.ajax({
// 		url: url,
// 		success: function(response) {
// 			callback(response);
// 		},
// 		error: function(e) {
// 			console.error("Failed to call " + url);
// 			callback(null);
// 		},
// 		async:true,
// 		timeout: 7500 // 7.5 seconds
// 	});
//
// }

// $.when(ajax1(), ajax2(), ajax3(), ajax4()).done(function(a1, a2, a3, a4){
//     // the code here will be executed when all four ajax requests resolve.
//     // a1, a2, a3 and a4 are lists of length 3 containing the response text,
//     // status, and jqXHR object for each of the four ajax calls respectively.
// });
//
// function ajax1() {
//     // NOTE:  This function must return the value
//     //        from calling the $.ajax() method.
//     return $.ajax({
//         url: "/search/Irene Fellner",
//         dataType: "json",
//         data:  yourJsonData,
//         ...
//     });
// }
//
// $.when(
//   // Get the HTML
//   $.get("/feature/", function(html) {
//     globalStore.html = html;
//   }),
//
//   // Get the CSS
//   $.get("/assets/feature.css", function(css) {
//     globalStore.css = css;
//   }),
//
//   // Get the JS
//   $.getScript("/assets/feature.js")
//
// ).then(function() {
//
//   // All is ready now, so...
//
//   // Add CSS to page
//   $("<style />").html(globalStore.css).appendTo("head");
//
//   // Add HTML to page
//   $("body").append(globalStore.html);
//
// });



// $.when(getRouteStartInfo(), getRouteEndInfo()).done(function(a1, a2){
//
//     console.log("WWWWWWWWWWWWWWWWWOOOOOOOOOOOOOOOOOOWWWWWWWWWWWWWWWWWWWWW");
//     // the code here will be executed when all four ajax requests resolve.
//     // a1, a2, a3 and a4 are lists of length 3 containing the response text,
//     // status, and jqXHR object for each of the four ajax calls respectively.
// });


// $.when(ajax1(), ajax2(), ajax3(), ajax4()).done(function(a1, a2, a3, a4){
//     // the code here will be executed when all four ajax requests resolve.
//     // a1, a2, a3 and a4 are lists of length 3 containing the response text,
//     // status, and jqXHR object for each of the four ajax calls respectively.
// });
//
// function ajax1() {
//     // NOTE:  This function must return the value
//     //        from calling the $.ajax() method.
//     return $.ajax({
//         url: "someUrl",
//         dataType: "json",
//         data:  yourJsonData,
//         ...
//     });
// }


// function getStart(routeStartText){
//     var url = '/search/'+ routeText;
//     return getResultFromURLWithCallback(url, callback)
// }
//
// // Generic function to make an AJAX call
// var fetchData = function(query, dataURL) {
//     // Return the $.ajax promise
//     return $.ajax({
//         data: query,
//         dataType: 'json',
//         url: dataURL
//     });
// }

// Generic function to make an AJAX call
var fetchData2 = function(text) {
    console.log("IN FETCHDATA 2 : " + text);
    // Return the $.ajax promise
    return $.ajax({

        dataType: 'json',
        url: "/search/" + text
    });
}

var fetcherMd = function(foo) {
    return $.ajax({
        dataType: 'json',
        url: '/search/' + foo
    }).done(function (data) {
        // If successful
        //console.log(data);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        // If fail
        //console.log(textStatus + ': ' + errorThrown);
    });
}

var runRouteM = function(startP, endP) {
    return $.ajax({
        dataType: 'json',
        url: '/directions/' + startP + endP
    }).done(function (data) {
        // If successful
        //console.log(data);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        // If fail
        //console.log(textStatus + ': ' + errorThrown);
    });
}

// var ajaxCall = $.ajax({
//     context: $(element),
//
//     dataType: 'json',
//     url: '/path/to/script'
// });
//
// ajaxCall.done(function(data) {
//     console.log(data);
// });

// var getOrder = fetchData(
//     {
//         'hash': '2528ce2ed5ff3891c71a07448a3003e5',
//         'email': 'john.doe@gmail.com'
//     }, '/path/to/url/1'),
//     getCustomerID = fetchData(
//     {
//         'email': 'john.doe@gmail.com'
//     }, '/path/to/url/2');

// Use $.when to check if both AJAX calls are successful



// function createRequest() {
//      try {
//        request = new XMLHttpRequest();
//      } catch (trymicrosoft) {
//        try {
//          request = new ActiveXObject("Msxml2.XMLHTTP");
//        } catch (othermicrosoft) {
//          try {
//            request = new ActiveXObject("Microsoft.XMLHTTP");
//          } catch (failed) {
//            request = null;
//          }
//        }
//      }
//
//      if (request == null)
//        alert("Error creating request object!");
//
//
//
// }

   // function getRouteStartInfo(routeStartText) {
  //    createRequest();
  //    request.open('GET', '/search/'+ routeStartText, true);
  //    request.onreadystatechange = runRouteQuery("start");
  //    request.send(null);
  // }
 //
 // function getRouteEndInfo(routeEndText) {
 //     createRequest();
 //     request.open('GET', '/search/'+ routeEndText, true);
 //
 //     request.onreadystatechange = runRouteQuery("end");
 //     request.send(null);
 //  }

//     function runRouteQuery(position) {
//
//     if (request.readyState == 4) {
//         var myVillages = JSON.parse(request.responseText);
//
//         if (position === 'start') {
//
//             routeLocalData.start = {};
//             routeLocalData.start.xcoord = myVillages.features[0].properties.centerGeometry.coordinates[0];
//             routeLocalData.start.ycoord = myVillages.features[0].properties.centerGeometry.coordinates[1];
//             routeLocalData.start.floor = myVillages.features[0].properties.floor_num;
//
//             // var xcoord = myVillages.features[0].properties.centerGeometry.coordinates[0];
//             // var ycoord = myVillages.features[0].properties.centerGeometry.coordinates[1];
//             // var floor = myVillages.features[0].properties.floor_num;
//             // var frontOffice = searchString.features[0].properties.frontoffice;
//
//             var routeStartValue = routeLocalData.start.xcoord + "," + routeLocalData.start.ycoord + "," + routeLocalData.start.floor;
//             routeLocalData.start.routeValue = routeStartValue;
//
//
//         } else if (position === "end") {
//
//             routeLocalData.end = {};
//             routeLocalData.end.xcoord = myVillages.features[0].properties.centerGeometry.coordinates[0];
//             routeLocalData.end.ycoord = myVillages.features[0].properties.centerGeometry.coordinates[1];
//             routeLocalData.end.floor = myVillages.features[0].properties.floor_num;
//
//             var routeEndValue = routeLocalData.end.xcoord + "," + routeLocalData.end.ycoord + "," + routeLocalData.end.floor;
//             routeLocalData.end.routeValue = routeEndValue;
//
//
//         }
//     }
// }

// // function getRouteToFromInfo(routeText, fromOrTo) {
// function getRouteToFromInfo(routeStartText, routeEndText) {
//
//     var myReq = new XMLHttpRequest();
//     myReq.open('GET', '/search/'+ routeText);
//     myReq.onload = function () {
//
//         if (myReq.status >= 200 && myReq.status < 400) {
//
//             var myVillages = JSON.parse(myReq.responseText);
//
//             if (fromOrTo==='start'){
//
//                 // renderHtml(myVillages);
//
//                 tempStart = [];
//
//
//                 routeLocalData.start = {};
//                 routeLocalData.start.xcoord = myVillages.features[0].properties.centerGeometry.coordinates[0];
//                 routeLocalData.start.ycoord = myVillages.features[0].properties.centerGeometry.coordinates[1];
//                 routeLocalData.start.floor = myVillages.features[0].properties.floor_num;
//
//                 var xcoord = myVillages.features[0].properties.centerGeometry.coordinates[0];
//                 var ycoord= myVillages.features[0].properties.centerGeometry.coordinates[1];
//                 var floor = myVillages.features[0].properties.floor_num;
//                 // var frontOffice = searchString.features[0].properties.frontoffice;
//
//                 var routeStartValue = routeLocalData.start.xcoord + "," + routeLocalData.start.ycoord + "," + routeLocalData.start.floor;
//                 routeLocalData.start.routeValue = routeStartValue;
//
//                 //tempStart.push(routeVal);
//                 //return routeVal;
//             // console.log('madata : ' + myVillages.features[0].properties.roomcode);
//             // console.log("geoms area: " + myVillages.features[0].properties.centerGeometry.coordinates)
//             }else if (fromOrTo==='end'){
//
//
//                 routeLocalData.end = {};
//                 routeLocalData.end.xcoord = myVillages.features[0].properties.centerGeometry.coordinates[0];
//                 routeLocalData.end.ycoord = myVillages.features[0].properties.centerGeometry.coordinates[1];
//                 routeLocalData.end.floor = myVillages.features[0].properties.floor_num;
//
//                 var routeEndValue = routeLocalData.end.xcoord + "," + routeLocalData.end.ycoord + "," + routeLocalData.end.floor;
//                 routeLocalData.end.routeValue = routeEndValue;
//
//
//             }
//
//         }
//         else {
//             console.log('error do something more usefull');
//         }
//     };
//
//     myReq.onerror = function () {
//         console.log("connection error");
//
//     }
//     myReq.send();
//
// }


// function get_end(searchWord1) {
//
//     var myReq = new XMLHttpRequest();
//     myReq.open('GET', '/search/'+ searchWord1);
//     myReq.onload = function () {
//
//         if (myReq.status >= 200 && myReq.status < 400) {
//             var myVillages = JSON.parse(myReq.responseText);
//             // renderHtml(myVillages);
//
//             tempEnd = [];
//
//                 var xcoord = myVillages.features[0].properties.centerGeometry.coordinates[0];
//                 var ycoord= myVillages.features[0].properties.centerGeometry.coordinates[1];
//                 var floor = myVillages.features[0].properties.floor_num;
//                 // var frontOffice = searchString.features[0].properties.frontoffice;
//
//                 var routeVal = xcoord + "," + ycoord + "," + floor;
//
//             tempEnd.push(routeVal);
//             // console.log('madata : ' + myVillages.features[0].properties.roomcode);
//             // console.log("geoms area: " + myVillages.features[0].properties.centerGeometry.coordinates)
//         }
//         else {
//             console.log('error do something more usefull');
//         }
//     };
//
//     myReq.onerror = function () {
//         console.log("connection error");
//
//     }
//     myReq.send();
//
// }



function getSearchRes(searchString) {
    // var aks = searchString.features[0].properties.aks_nummer;
    // var xman = searchString.features[0].properties.roomcode;
    var xcoord = searchString[0].features[0].properties.centerGeometry.coordinates[0];
    var ycoord= searchString[0].features[0].properties.centerGeometry.coordinates[1];
    var floor = searchString[0].features[0].properties.floor_num;
    // var frontOffice = searchString.features[0].properties.frontoffice;

    var routeVal = xcoord + "," + ycoord + "," + floor;


    // console.log("WOOOOW ROOMCODE is   "+ searchString.features[0].properties.roomcode)
    // console.log("WOOOOW AKS is   "+ searchString.features[0].properties.aks_nummer)
    // console.log("ROUTE value is   "+ routeVal)



    return routeVal;




}