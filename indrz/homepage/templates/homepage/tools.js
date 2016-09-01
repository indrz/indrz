if (typeof console == "undefined" || console.log == undefined || console.info == undefined || console.error == undefined) {
    var console =
    {
        log: function () {
        },
        info: function () {
        },
        error: function () {
        }
    };
}

function getResultFromURL(url) {
    var retStr = "";

    jQuery.ajax({
        url: url,
        success: function (response) {
            retStr = response;
        },
        error: function (e) {
            res = null;
            console.error("Failed to call " + url);
        },
        async: false,
        timeout: 7500 // 7.5 seconds
    });

    return retStr;
}

function indrzApiCall(url, callback) {

    jQuery.ajax({
        url: url,
        //data: JSON.stringify(data),
        //data: data,
        type: 'POST',
        dataType: "json",
        contentType: 'application/json; charset=UTF-8',
        success: function (jsonObj) {
            callback(jsonObj.result);
        },
        error: function (e) {
            console.error("Failed to do json rpc call to " + url );
            callback(null);
        },
        async: true,
        timeout: 7500 // 7.5 seconds
    });
}



function jsonRpcCall(url, methodName, parameters, callback) {
    data = '{"method": "' + methodName + '", "id": "labla", "params": [' + parameters + '], "jsonrpc":"2.0"}';

    jQuery.ajax({
        url: url,
        //data: JSON.stringify(data),
        data: data,
        type: 'POST',
        dataType: "json",
        contentType: 'application/json; charset=UTF-8',
        success: function (jsonObj) {
            callback(jsonObj.result);
        },
        error: function (e) {
            console.error("Failed to do json rpc call to " + url + " with methodName " + methodName);
            callback(null);
        },
        async: true,
        timeout: 7500 // 7.5 seconds
    });
}

function getResultFromURLWithCallback(url, callback) {

    jQuery.ajax({
        url: url,
        success: function (response) {
            callback(response);
        },
        error: function (e) {
            console.error("Failed to call " + url);
            callback(null);
        },
        async: true,
        timeout: 7500 // 7.5 seconds
    });

}
