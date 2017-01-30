
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



// function getSearchRes(searchString) {
//     // var aks = searchString.features[0].properties.aks_nummer;
//     // var xman = searchString.features[0].properties.roomcode;
//     var xcoord = searchString[0].features[0].properties.centerGeometry.coordinates[0];
//     var ycoord= searchString[0].features[0].properties.centerGeometry.coordinates[1];
//     var floor = searchString[0].features[0].properties.floor_num;
//     // var frontOffice = searchString.features[0].properties.frontoffice;
//
//     var routeVal = xcoord + "," + ycoord + "," + floor;
//
//
//     // console.log("WOOOOW ROOMCODE is   "+ searchString.features[0].properties.roomcode)
//     // console.log("WOOOOW AKS is   "+ searchString.features[0].properties.aks_nummer)
//     // console.log("ROUTE value is   "+ routeVal)
//
//
//
//     return routeVal;
//
//
//
//
// }



// s routing.js
    // var startVals = get_start(startSearchText);
    // var endVals = get_start(endSearchText);


    // var geoJsonUrl = baseApiRoutingUrl + 'start_coord=' + aksStart + '&endstr=' + aksEnd + '/?format=json';
    //
    // var routeUrl = baseApiRoutingUrl + "1826657.11148431,6142529.11906656,4&1826685.08369027,6142499.12539894,4&1"
    // var geoJsonUrl = baseApiRoutingUrl + xStart + "," + yStart + "," + floorStart + "&" + xEnd + "," + yEnd + "," + endFloor + "&" + routeType;
    //var geoJsonUrl = baseApiRoutingUrl + startVals + "&" + endVals + "&" + 0;
    // var geoJsonUrl = baseApiRoutingUrl + 'start_coord=' + routeLocalData.start.routeValue + '&enstr='+ routeLocalData.end.routeValue + '/?format=json';


// function getDirections(){
//
//     var customer = {contact_name :"Scott",company_name:"HP"};
//     $.ajax({
//         type: "POST",
//         data :JSON.stringify(customer),
//         url: "api/Customer",
//         contentType: "application/json"
//     });
//
// }


// function getDirections2(xStart, yStart, floorStart, xEnd, yEnd,endFloor, routeType) {



    //
    // $.getJSON(geoJsonUrl, function(json){
    //     destinationPoiInfo = json.route_info[0].destination.name;
    // });

       // var myD =  $.getJSON(geoJsonUrl, function(data) {
       //                   var n = data.route_info[0].destination.name;
       //                  console.log("xxxxxxxxx x  :  " + n);
       //
       //                  destinationPoiInfo.push(n);
       //
       //                  return n
       //                  //data is the JSON string
       //              });

       // console.log("PPPPPPPPPPPPPPPPP " + destinationPoiInfo);
       //
       // document.getElementById('route-to').value = destinationPoiInfo;



