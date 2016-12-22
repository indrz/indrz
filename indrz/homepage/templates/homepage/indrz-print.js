/**
 * Created by mdiener on 19.12.2016.
 */

function getScale(){
    var mapSizePixels = map.getSize()[0]-map.getSize()[1]
    var mapWidthPixels = map.getSize()[0]
    var mapHeightPixels = map.getSize()[1]
    var mapExtent = map.getView().calculateExtent(map.getSize())
    var xScreenDist = mapExtent[2] - mapExtent[0]
    var pxPerMeter = map.getView().getResolution()  // resoltuion is is the size of 1 pixel in map units
    var scaleVal = mapWidthPixels * pxPerMeter ;
    console.log(scaleVal);



    // var curZoom = map.getView().getZoom()
    // var scaleValue = 500
    //
    // if (curZoom >= 21){
    //     scaleValue == 500
    // }
    // else {
    //     scaleValue == 1500
    // }

    return scaleVal*2;

}

function createPrintRequest(){
    // var print_layers = "";
    // for (var i = 0; i < map.layers.length; i++) {
    //     if(map.layers[i].visibility == true){
    //         //get a string of visible layers
    //         print_layers = print_layers + map.layers[i].name + ','
    //     }
    // }
    // //remove the trailing ','
    // print_layers = print_layers.slice(0, -1);
    // console.log(print_layers);

    var center_coord = map.getView().getCenter();
    var mapScale = getScale();

var matrixIds= [
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

    var spec = {
        layout: 'A4',
        mapTitle: 'WU Campus Plan',
        comment: 'some comment',
        id: "foo-id",
        nameBorderColor :'black',
        nameBackgroundColor : 'red',
        disableScaleLocking: true,
        srs: 'EPSG:3857',
        units: 'meters',
        geodetic: false,
        outputFilename: 'WU-Plan-${yyyyMMdd}.pdf',
        outputFormat: 'pdf',
        // mergeableParams: {
        //     cql_filter: {
        //         defaultValue: 'INCLUDE',
        //         separator: ';',
        //         context: 'http://labs.metacarta.com/wms/vmap0'
        //     }
        // },
        layers: [
            {
                type: 'WMS',
                layers: ['indrz:e00'],
                baseURL: 'http://gis-neu.wu.ac.at:8080/geoserver290/indrz/wms',
                format: 'image/jpeg'
            }
            // {
            //     type: 'WMTS',
            //     baseURL: 'https://maps1.wien.gv.at/basemap/{Layer}/{Style}/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}.png',
            //     layer: 'bmapgrau',
            //     matrixSet: 'google3857',
            //     matrixIds: matrixIds
            //
            // },
            // {
            //     "baseURL": "http://wmts0.geo.admin.ch/",
            //     "opacity": 1,
            //     "singleTile": false,
            //     "customParams": {},
            //     "type": "WMTS",
            //     "layer": "ch.swisstopo.pixelkarte-farbe",
            //     "version": "1.0.0",
            //     "requestEncoding": "REST",
            //     "tileOrigin": [420000, 350000],
            //     "tileSize": [256, 256],
            //     "style": "default",
            //     "formatSuffix": "jpeg",
            //     "dimensions": ["TIME"],
            //     "params": {
            //         "TIME": "20120809"
            //     },
            //     "maxExtent": [420000, 30000, 900000, 350000],
            //     "matrixSet": "21781",
            //     "zoomOffset": 0,
            //     "resolutions": [4000, 3750, 3500, 3250, 3000, 2750, 2500, 2250, 2000, 1750, 1500, 1250, 1000, 750, 650, 500, 250, 100, 50, 20, 10, 5, 2.5, 2, 1.5, 1, 0.5]
            // }
        ],
        pages: [
            {
                // center: [1826602.52731,6142514.228525],
                center: center_coord,
                scale: mapScale,
                dpi: 150,
                geodetic: false,
                strictEpsg4326: false
                // ...CUSTOM_PARAMS...
            }
        ]
    }

// var testUrl  = "gis-neu.wu.ac.at:8080/geoserver290/pdf/print.pdf?spec={"units":"meters","srs":"EPSG:3857","layout":"A4","dpi":"75","maptitle":"This is the map title","comment":"This is the map comment","resourcesUrl": "http://gis-neu.wu.ac.at:8080/img","layers":[{"baseURL":"http://gis-neu.wu.ac.at:8080/geoserver290/workspace/wms","opacity":1,"singleTile":true,"type":"WMS","layers":["' + layers + '"],"format":"image/jpeg","styles":[""]}],"pages":[{"center":[' + map.getCenter().lon + ',' + map.getCenter().lat + '],"scale":' + getMapScale(Math.ceil(map.getScale())) + ',"rotation":0}]}'



// var specs = {"units":"degrees",
//     "srs":"EPSG:4326",
//     "layout":"A4",
//     "dpi":"300",
//     "maptitle":"This is the map title",
//     "comment":"This is the map comment",
//     "resourcesUrl": "http://gis-neu.wu.ac.at:8080/img",
//     "layers":[{"baseURL":"http://gis-neu.wu.ac.at:8080/geoserver290/workspace/wms",
//         "opacity":1,
//         "singleTile":true,
//         "type":"WMS",
//         "layers":["' + layers + '"],"format":"image/jpeg","styles":[""]}],
//     "pages":[{"center":[' + map.getCenter().lon + ',' + map.getCenter().lat + '],"scale":' + getMapScale(Math.ceil(map.getScale())) + ',"rotation":0}]}
//
// var maptitle= "This is the map title";
// var mapcomment= "This is the map comment";
// // var printurl = "http://gis-wu.ac.at:8080/geoserver290/pdf/print.pdf?spec={"units":"degrees","srs":"EPSG:4326","layout":"A4","dpi":"300","maptitle":"This is the map title","comment":"This is the map comment","resourcesUrl": "http://gis-neu.wu.ac.at:8080/img","layers":[{"baseURL":"http://gis-neu.wu.ac.at:8080/geoserver290/workspace/wms","opacity":1,"singleTile":true,"type":"WMS","layers":["' + layers + '"],"format":"image/jpeg","styles":[""]}],"pages":[{"center":[' + map.getCenter().lon + ',' + map.getCenter().lat + '],"scale":' + getMapScale(Math.ceil(map.getScale())) + ',"rotation":0}]}'
    console.log(spec);
    console.log("print spec");
    var printUrl = "http://gis-neu.wu.ac.at:8080/geoserver290/pdf/print.pdf?spec=" + JSON.stringify(spec);
    $("#id-export-png").attr("href", printUrl);
// http://gis-wu.ac.at:8080/geoserver290/pdf/print.pdf?spec={"layout":"A4 portrait","srs":"EPSG:3857","units":"meters","geodetic":false,"outputFilename":"political-boundaries","outputFormat":"pdf","layers":[{"type":"WMS","layers":["indrz:e00"],"baseURL":"http://gis-neu.wu.ac.at:8080/geoserver290/indrz/wms","format":"image/jpeg"}],"pages":[{"center":[1826602.52731,6142514.228525],"scale":4000000,"dpi":75,"geodetic":false,"strictEpsg4326":false}],"legends":[{"classes":[{"icons":["full url to the image"],"name":"an icon name","iconBeforeName":true}],"name":"a class name"}]}
    return printUrl;

};




// $("#btnprint").attr("href", printUrl);
// $('#btnprint')[0].click();



$('#id-export-png').on('click', function() {


    // var dims = {
    //     a0: [1189, 841],
    //     a1: [841, 594],
    //     a2: [594, 420],
    //     a3: [420, 297],
    //     a4: [297, 210],
    //     a5: [210, 148]
    //   };
    //
    // var format = 'a4';
    // var dim = dims[format];
    //
    console.log("bitte2");
    console.log(createPrintRequest());
    //     map.once('postcompose', function(event) {
    //       var canvas = event.context.canvas;
    //       var pdf = new jsPDF('landscape', undefined, format);
    //       canvas.toBlob(function(blob) {
    //         // pdf.addImage(blob, 'PNG', 0, 0, dim[0], dim[1]);
    //         // pdf.save('WU-Campus-Plan.pdf');
    //         saveAs(blob, 'WU_campus_plan.png');
    //       });
    //     });
    //     map.renderSync();
      });

        //
        // var tileLoadEnd = function() {
        //   ++loaded;
        //   if (loading === loaded) {
        //     var canvas = this;
        //     window.setTimeout(function() {
        //       loading = 0;
        //       loaded = 0;
        //       // var data = canvas.toDataURL('image/png');
        //         var data = canvas.toBlob(function(blob){});
        //       var pdf = new jsPDF('landscape', undefined, format);
        //       pdf.addImage(data, 'JPEG', 0, 0, dim[0], dim[1]);
        //       pdf.save('WU-Campus-Plan.pdf');
        //       source.un('tileloadstart', tileLoadStart);
        //       source.un('tileloadend', tileLoadEnd, canvas);
        //       source.un('tileloaderror', tileLoadEnd, canvas);
        //       map.setSize(size);
        //       map.getView().fit(extent, size);
        //       map.renderSync();
        //       // exportButton.disabled = false;
        //       document.body.style.cursor = 'auto';
        //     }, 100);
        //   }
        // };
        //
        // map.once('postcompose', function(event) {
        //   source.on('tileloadstart', tileLoadStart);
        //   source.on('tileloadend', tileLoadEnd, event.context.canvas);
        //   source.on('tileloaderror', tileLoadEnd, event.context.canvas);
        // });
        //
        // map.setSize([width, height]);
        // map.getView().fit(extent, /** @type {ol.Size} */ (map.getSize()));
        // map.renderSync();

      // }, false);
      //
      // });






    // console.log("inf print method");

  // map.once('postcompose', function (event) {
  //     var canvas = event.context.canvas;
  //     canvas.toBlob(function (blob) {
  //         saveAs(blob, 'map.png');
  //     });
  // });
  // map.renderSync();
// })

