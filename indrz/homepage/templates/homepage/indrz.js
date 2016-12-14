var indrz = {};


indrz.whatsHere = function (coordinates, whatsHereCallback) {
    q = '{"coordinates": {"lon": ' + coordinates.lon + ', "lat": ' + coordinates.lat + ', "layer": ' + coordinates.layer + ' } }'

    var res = jsonRpcCall(webserviceBaseUrl, webserviceWhatsHereMethod, q,
        function tmpCallback(res) {
            return function (res, callbackMethod) {
                if (res == null || res == "") {
                    console.info("webservice returned nothing...");
                }
                else {
                    //console.info("Webservice result was: " + res);
                    callbackMethod(res);
                    return;
                }
                callbackMethod(null);
                return;
            }(res, whatsHereCallback);
        }
    );
}


indrz.whatsHerePoi = function (coordinates, whatsHereCallback) {
    q = '{"coordinates": {"lon": ' + coordinates.lon + ', "lat": ' + coordinates.lat + ', "layer": ' + coordinates.layer + ' } }'

    var res = jsonRpcCall(webserviceBaseUrl, webserviceWhatsHerePOIMethod, q,
        function tmpCallback(res) {
            return function (res, callbackMethod) {
                if (res == null || res == "") {
                    console.info("webservice returned nothing...");
                }
                else {
                    //console.info("Webservice result was: " + res);
                    callbackMethod(res);
                    return;
                }
                callbackMethod(null);
                return;
            }(res, whatsHereCallback);
        }
    );
}

