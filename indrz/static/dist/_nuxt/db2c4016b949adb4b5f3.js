(window.webpackJsonp=window.webpackJsonp||[]).push([[7],{358:function(e,t,o){var content=o(416);"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,o(12).default)("5125b290",content,!0,{sourceMap:!1})},359:function(e,t,o){var content=o(418);"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,o(12).default)("08044eb0",content,!0,{sourceMap:!1})},362:function(e,t,o){"use strict";o(40);var r=o(13),n=(o(25),o(77),o(48),o(528)),c=o(599),l=o(529),d=o(391),f=o(466),m=o(495),h=o(337),y=o(500),v=o(494),w=o(425),P=o(357),_=o(365),C=o(381),x=o(354),I=o(386),k=o(393),S=o(420),L=o(456),E=o(327),O=o(369),F=o(371),$=o(131),N=o(78),M=o(385),T=function(e,t,o,r){var n=Object(h.d)("EPSG:3857"),c="{Layer}/{Style}/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}"+t,l=["https://maps1.wien.gv.at/basemap/"+c,"https://maps2.wien.gv.at/basemap/"+c,"https://maps3.wien.gv.at/basemap/"+c,"https://maps4.wien.gv.at/basemap/"+c],d=new w.b({origin:[-20037508.3428,20037508.3428],extent:[977650,5838030,1913530,6281290],resolutions:[156543.03392811998,78271.51696419998,39135.758481959994,19567.879241008,9783.939620504,4891.969810252,2445.984905126,1222.9924525644,611.4962262807999,305.74811314039994,152.87405657047998,76.43702828523999,38.21851414248,19.109257071295996,9.554628535647998,4.777314267823999,2.3886571339119995,1.1943285669559998,.5971642834779999,.29858214174039993,.14929107086936],matrixIds:["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]}),f=new v.a({tilePixelRatio:1,projection:n,layer:e,style:"normal",matrixSet:"google3857",urls:l,crossOrigin:"anonymous",requestEncoding:"REST",tileGrid:d,attributions:'© <a href="https://www.basemap.at/">Basemap.at       </a>'});return new y.a({name:e,source:f,minResolution:.298582141738,visible:o,type:"background"})},V=function(e){e.forEach(function(e){return e.setVisible(!1)})},z=function(e,t,map){if(t.length>0){var o=t.find(function(t){var o=t.getProperties();return(o.name||o.floorName).toLowerCase()===e.toLowerCase()});o&&(o.setVisible(!0),map.getLayers().forEach(function(e){if("RouteFromSearch"===e.get("name")){var t=o.getProperties().floorName;e.getSource().getFeatures().forEach(function(e){e.getProperties().floor_name===t?e.setStyle(O.a.routeActiveStyle):e.setStyle(O.a.routeInactiveStyle)})}}))}},R=function(e,t,map){var o=e?e.getProperties().floorName:"",r=t.switchableLayers.find(function(e){return e.getProperties().floorName===o});r&&H(r.getProperties().name,t.switchableLayers,map)},B=function(e,t,o,r,n,c,l){l=l||0;var d="",f="",m="";c=c||0;return 0===c?f="searchResListItem_"+e:(f="searchResListItem_"+e+"-"+c,d='<img src="'+l+'" alt="POI" style="height: 25px; padding-right:5px;">'),m='<a href="#" onclick="showRes('+t+","+o+","+c+')" id="'+f+'" class="list-group-item indrz-search-res" >'+r+' <span class="badge">Floor '+n+"</span> </a>",""!==l&&(m='<a href="#" onclick="showRes('+t+","+o+","+c+')" id="'+f+'" class="list-group-item indrz-search-res" >  '+d+r+' <span class="badge">Floor '+n+"</span> </a>"),m},image=new k.a({anchor:[.5,46],anchorXUnits:"fraction",anchorYUnits:"pixels",src:"/static/homepage/img/other.png"}),j={Point:[new x.c({image:image})],LineString:[new x.c({stroke:new I.a({color:"#68ff5b",width:1})})],MultiLineString:[new x.c({stroke:new I.a({color:"#68ff5b",width:1})})],MultiPoint:[new x.c({image:image})],MultiPolygon:[new x.c({stroke:new I.a({color:"#4ff0ff",width:3}),fill:new S.a({color:"rgba(38, 215, 255, 0.4)"})})],Polygon:[new x.c({stroke:new I.a({color:"#4ff0ff",width:3}),fill:new S.a({color:"rgba(38, 215, 255, 0.4)"})})],GeometryCollection:[new x.c({stroke:new I.a({color:"magenta",width:2}),fill:new S.a({color:"magenta"}),image:new L.a({radius:10,fill:null,stroke:new I.a({color:"magenta"})})})],Circle:[new x.c({stroke:new I.a({color:"red",width:2}),fill:new S.a({color:"rgba(255,0,0,0.2)"})})]},A=function(e,t){var o=e.getGeometry().getType();if("MultiPolygon"===o)return j[e.getGeometry().getType()];if("MultiPoint"===o){var r=new k.a({anchor:[.5,46],anchorXUnits:"fraction",anchorYUnits:"pixels",src:e.get("icon"),opacity:1});return new x.c({image:r})}},D=function(){var e=Object(r.a)(regeneratorRuntime.mark(function e(t){var o,r;return regeneratorRuntime.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return o="".concat(N.a.searchUrl,"/").concat(t),e.next=3,$.a.request({url:o});case 3:return r=e.sent,e.abrupt("return",r.data);case 5:case"end":return e.stop()}},e)}));return function(t){return e.apply(this,arguments)}}(),U=function(){var e=Object(r.a)(regeneratorRuntime.mark(function e(map,t,o,r,n,c,l,d,f,m,h,y,v,w,x,I){var k,S,L,O,$,N,M,T,V;return regeneratorRuntime.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:if(r&&map.removeLayer(r),k=new P.a,S=[],L={},I){e.next=10;break}return e.next=7,D(c);case 7:L=e.sent,e.next=11;break;case 10:L=I;case 11:return O=new C.a,$=O.readFeatures(L,{featureProjection:"EPSG:4326"}),k.addFeatures($),k.forEachFeature(function(e){var t=e.get("name"),r=e.getGeometry().getExtent(),n=Object(E.x)(r),l=c,d=l=c===t?c:t,f=e.get("floor_name")?e.get("floor_name").toLowerCase():"",m=e.get("category_en"),h=e.get("roomcode"),y="";y=l!==h?" ("+h+")":"";var v="",w="";e.getProperties().hasOwnProperty("poi_id")?(v=e.get("poi_id"),w=e.get("icon"),o.poiId=e.get("poi_id"),o.src=e.get("src")):(o.poiId="noid",o.src=e.get("src"));var P='"'+l+'"';if(""!==m&&void 0!==m){var _=d+" ("+m+")";S.push(B(l,P,n,_,f,v,w))}else if(""!==h&&void 0!==h){var C=d+y;S.push(B(l,P,n,C,f,v,w))}else{var x=d;S.push(B(l,P,n,x,f,v,w))}}),N=Object(E.x)(k.getExtent()),M="",T="",1===$.length?(F.a.openIndrzPopup(o,d,f,m,h,y,v,w,x,$[0].getProperties(),N,$[0]),G(map.getView(),N,l),T=$[0].getProperties().floor_name?$[0].getProperties().floor_name.toLowerCase():"",M=t.switchableLayers.find(function(e){return e.getProperties().floorName===T}),R(M,t,map)):0===$.length?("<p href='#' class='list - group - item indrz - search - res'> Sorry nothing found</p>",console.log("<p href='#' class='list - group - item indrz - search - res'> Sorry nothing found</p>")):(V=k.getExtent(),map.getView().fit(V),map.getView().setZoom(l)),r=new _.a({source:k,style:A,title:"SearchLayer",name:"SearchLayer",zIndex:999}),map.getLayers().push(r),window.location.href="#map",e.abrupt("return",{searchLayer:r,floorName:T,searchResult:S});case 23:case"end":return e.stop()}},e)}));return function(t,o,r,n,c,l,d,f,m,h,y,v,w,P,_,C){return e.apply(this,arguments)}}(),G=function(view,e,t){view.animate({center:e,duration:2e3,zoom:t})},H=function(e,t,map){V(t),z(e,t,map),M.a.setPoiFeatureVisibility(map,e)};t.a={getStartCenter:function(){return N.a.defaultCenterXY},getMapControls:function(){return[new n.a({collapsible:!1}),new c.a,new l.a({target:"zoom-control"})]},getWmsLayers:function(e){var t=[];e.forEach(function(e,o){var r=e.short_name.toLowerCase(),n=N.a.layerNamePrefix+r,c=function(e,t,o,r,n){return new f.a({source:new m.a({url:N.a.baseWmsUrl,params:{LAYERS:t,TILED:!0},serverType:"geoserver",crossOrigin:""}),visible:r,name:e,floorNumber:o,floorName:e.split(N.a.layerNamePrefix)[1],type:"floor",zIndex:n,crossOrigin:"anonymous"})}(n,N.a.geoServerLayerPrefix+n,e.floor_num,0===o,3);t.push(c)});var o=new d.a({layers:t,name:"wms floor maps"});return{layers:t,layerGroup:o}},getLayers:function(){var e=T("bmapgrau",".png",!0),t=T("bmaporthofoto30cm",".jpg",!1);return{baseLayers:{ortho30cmBmapat:t,greyBmapat:e},switchableLayers:[],layerGroups:[new d.a({layers:[e,t],name:"background maps"}),new d.a({layers:[],id:99999,name:"poi group"}),new d.a({layers:[],id:900,name:"campus locations"})]}},hideLayers:V,setLayerVisible:z,activateFloor:R,activateLayer:H,searchIndrz:U,zoomer:G}},369:function(e,t,o){"use strict";o(22);var r=o(354),n=o(386),c=o(393),l=new r.c({image:new c.a({src:"/media/poi_icons/route_marker_C.png",anchor:[.5,1]}),zIndex:6}),d=new r.c({image:new c.a({src:"/media/poi_icons/flag.png",anchor:[.5,1]}),zIndex:6}),f=new r.c({image:new c.a({src:"/media/poi_icons/flag-checkered.png",anchor:[.5,1]}),zIndex:6}),m=new r.c({stroke:new n.a({color:"#ba4682",width:4}),zIndex:6}),h=new r.c({stroke:new n.a({color:"#ba4682",width:2,lineDash:[.1,5],opacity:.5}),zIndex:6});t.a={routeActiveStyle:m,routeInactiveStyle:h,routeMarkerCStyle:l,faCircleSolidStyle:d,faFlagCheckeredStyle:f,setPoiStyleOnLayerSwitch:function(e,t){var o="http://localhost:8000/media/poi_icons/"+e,n=new r.c({image:new c.a({anchor:[.5,46],anchorXUnits:"fraction",anchorYUnits:"pixels",opacity:.4,src:o})}),l=new r.c({image:new c.a({anchor:[.5,46],anchorXUnits:"fraction",anchorYUnits:"pixels",opacity:1,src:o})});return t?l:n},createPoiStyle:function(e,t){var o="http://localhost:8000/media/poi_icons/"+e,n=new r.c({image:new c.a({anchor:[.5,46],anchorXUnits:"fraction",anchorYUnits:"pixels",opacity:.4,src:o})}),l=new r.c({image:new c.a({anchor:[.5,46],anchorXUnits:"fraction",anchorYUnits:"pixels",src:o})});return"y"===t?["education_active","access_active","security_active","infrastructure_active","services_active"].includes(e)?n:l:n}}},371:function(e,t,o){"use strict";o(48),o(25);var r=o(78),n=window.location.href,c=function(e,t){var o="",r="";if(e.hasOwnProperty("room_code")&&e.room_code&&(r=e.room_code,o=e.room_code),e.hasOwnProperty("name")&&e.name)return o=e.name;if(e.hasOwnProperty("name_de")&&e.name_de)return o="de"===t?e.name_de:e.name||e.name_en;if(e.hasOwnProperty("short_name")){if(e.short_name)return o=e.short_name;if(r)return o=r}if(e.hasOwnProperty("label")){if(e.label)return o=e.label;if(r)return o=r}if(e.hasOwnProperty("key")){if(e.key)return o=e.key;if(r)return o=r}if(e.hasOwnProperty("campus_name")){if(e.campus_name)return o=e.campus_name;if(r)return o=r}return e.hasOwnProperty("room_external_id")&&e.room_external_id&&!o?o=e.room_external_id:e.room_code?o=e.room_code:o},l=function(p){if(p.hasOwnProperty("roomcode")){if(p.roomcode)return p.roomcode.split(".")[0]}else if(p.hasOwnProperty("building_name")&&(null!==p.building_name||""!==p.building_name||void 0!==p.building_name))return p.building_name;return""},d=function(e,t,o){"popupHomepage"===o&&(t='<a target="_blank" href="'+t+'">'+t+"</a>");var r=document.getElementById("popupTable").insertRow(0),n=r.insertCell(0),c=r.insertCell(1);n.innerHTML=e,c.innerHTML=t,n.setAttribute("class","no-wrap"),c.setAttribute("id",o)},f=function(e,map,t,o,r,c){var l=map.getView().calculateExtent(map.getSize()),d=map.getView().getZoom(),f=map.getView().getCenter(),m=f[0],h=f[1],y="/?campus=1&centerx="+m+"&centery="+h+"&zlevel="+d+"&floor="+c,data={};if("route"===e)y=o.routeUrl?o.routeUrl:"noid"!==o.startPoiId&&"noid"!==o.endPoiId||"noid"!==t.poiId?o.routeUrl:("undefined"===t.poiId&&""===t.poiId&&t.poiId,"/?campus=1&startstr="+o.startName+"&endstr="+o.endName);else if("search"===e)t.hasOwnProperty("external_id")&&(y=t.external_id===t.name?"/?campus=1&q="+t.external_id:"/?campus=1&q="+t.name),y=r.searchText?"/?campus=1&q="+r.searchText:"/?campus=1&q="+t.name;else if("map"===e)y="/?campus=1&centerx="+m+"&centery="+h+"&zlevel="+d+"&floor="+c;else if("bookId"===e)y=n+o.routeUrl;else{if("poiCatId"===e)return y=location.origin+"?"+t.poiCatShareUrl,{type:"poi",singlePoiUrl:location.origin+"?poi-id="+t.poiId+"&floor="+t.floor,poiCatUrl:y};y="wmsInfo"===e?n+"?campus=1&q="+t.wmsInfo:location.href}return data.extent=l,data.zoom=d,history.pushState(data,"live_url_update",y),location.href};t.a={closeIndrzPopup:function(e,t){for(var o in e.setPosition(void 0),t)t[o]=null;return e.setPosition(void 0),t.poiId="noid",t.poiCatId="noid",t.bookId=!1,t.bookCoords=!1,t.name=!1,!1},openIndrzPopup:function(e,t,o,f,m,h,y,v,w,P,_,C,x){var I=v.split(r.a.layerNamePrefix)[1].toUpperCase(),k=document.getElementById("popup-content");for(var S in e)e[S]=null;C=null!=C?C:-1,x=void 0!==x?x:[0,0],P.hasOwnProperty("poiId")&&(e.src="poi",e.poiId=P.poiId),P.hasOwnProperty("category")&&(e.src="poi",e.poiCatId=P.category),P.hasOwnProperty("spaceid")&&(e.spaceid=P.spaceid),P.hasOwnProperty("homepage")&&P.homepage&&P.homepage,P.hasOwnProperty("src")&&P.src&&(e.src=P.src),P.hasOwnProperty("space_type_id")&&(P.hasOwnProperty("src")&&(P.src?e.src=P.src:e.src="wms"),P.hasOwnProperty("id")&&(e.spaceid=P.id),P.hasOwnProperty("room_external_id")&&P.room_external_id&&(e.external_id=P.room_external_id)),P.hasOwnProperty("room_code")&&(e.wmsInfo=P.room_code,P.roomcode=P.room_code),P.hasOwnProperty("poi_id")?(P.poi_id,e.poiId=P.poi_id,P.hasOwnProperty("category")&&(e.poiCatId=P.category,e.poiCatName="de"===f?P.category_name_de:P.category_name_en,e.poiCatShareUrl=n+"?poi-cat-id="+e.poiCatId)):-1!==C&&"noid"===e.poiId&&"string"!=typeof C&&C.getId()&&(e.poiId=C.getId(),e.poiIdPopup=C.getId(),C.get("category")&&(e.poiCatId=C.get("category"),e.poiCatName="de"===f?C.get("category_name_de"):C.get("category_name_en"),e.poiCatShareUrl=n+"?poi-cat-id="+e.poiCatId)),"noid"!==e.poiId&&(e.poiCatShareUrl="poi-cat-id="+e.poiCatId),m=(m=_)||""!==m?_:P.centerGeometry.coordinates;var L,E=l(P),O=null,F=null;P.hasOwnProperty("category_de")&&P.category_de&&(F="de"===f?P.category_de:P.category_en),P.hasOwnProperty("room_description")?P.name=P.room_description:P.hasOwnProperty("short_name")&&(P.name=P.short_name),P.hasOwnProperty("room_code")&&(P.roomcode=P.room_code),L=c(P,f),!0===P.hasOwnProperty("centroid")&&P.centroid,O=(P.label,P.roomcode);k.innerHTML='<h4 style="user-select: text;">'+L+"</h4>",k.innerHTML+="<div><p>",k.innerHTML+='<table id="popupTable" style="user-select: text;"></table>',P.hasOwnProperty("campus_name")||(void 0!==P.building_name&&""!==P.building_name&&d("Building: ",E,"popupBuilding"),P.hasOwnProperty("shelfID")&&d("Building: ",P.building,"popupBuilding"),O&&d("Room Number: ",O,"popupRoomCode"),F&&d("Category: ",F,"popupRoomCat"),P.room_external_id&&d("Room Code",P.room_external_id,"popupSpaceAks"),d("Floor Name: ",I,"popupFloorNumber")),e.roomcode?e.roomcode:O||e.name&&e.name,k.innerHTML+="</p></div>",e.name=L,e.coords=m,e.floor=v,e.roomcode=O,w.setPosition(_),w.setOffset(x)},getTitle:c,getBuildingLetter:l,addPoiTableRow:d,getRoomInfo:function(e,t){var o;return t.switchableLayers.forEach(function(element){e===r.a.layerNamePrefix+element.getProperties().floorName&&(o=element.getSource())}),o},handleShareClick:function(map,e,t,o,r,n){var param="";return n?param="route":e.bookId?param="bookId":o.searchText?param="search":e.poiCatId?param="poiCatId":"wms"===e.src&&(param="wmsInfo"),f(param,map,e,t,o,r)},updateUrl:f}},385:function(e,t,o){"use strict";o(25);var r=o(357),n=o(365),c=o(381),l=o(391),d=o(327),f=o(369),m=o(362),h=o(371),y=o(78),v=o(131),w=function(data,e,t){var o="",l=new r.a,d=(new c.a).readFeatures(data,{featureProjection:"EPSG:4326"});return l.addFeatures(d),new n.a({source:l,style:function(e){var r=e.getProperties().floor_name;o=e.getProperties().name_en;var n=e.getProperties().category_icon_css_name;y.a.layerNamePrefix+r.toLowerCase()===t?e.setStyle(f.a.createPoiStyle(n,"y",r)):e.setStyle(f.a.createPoiStyle(n,"n",r))},title:o,name:o,id:e,active:!0,visible:!0,zIndex:999})};t.a={createPoilayer:w,poiExist:function(e,map){var t=void 0!==e.name?e.name:0,o=e.id,r=!1;return map.getLayers().forEach(function(e,i){e instanceof l.a&&e.getLayers().forEach(function(e,i){e.getProperties().id!==o&&e.getProperties().name!==t||(r=!0)})}),r},disablePoiById:function(e,map){map.getLayers().forEach(function(t,i){t instanceof l.a&&99999===t.getProperties().id&&t.getLayers().forEach(function(t){t.getProperties().id===e&&t.setVisible(!1)})})},removePoiById:function(e,map){map.getLayers().forEach(function(t,i){t instanceof l.a&&99999===t.getProperties().id&&t.getLayers().forEach(function(t){t.getProperties().id===e&&(t.setVisible(!1),map.removeLayer(t))})})},setPoiVisibility:function(e,map){map.getLayers().forEach(function(t){t instanceof l.a&&t.getLayers().forEach(function(t,i){t.getProperties().id===e&&(!0===t.getVisible()?t.setVisible(!1):t.setVisible(!0))})})},fetchPoi:function(e,map,t){return v.a.request({endPoint:"poi/cat/".concat(e,"/?format=json")}).then(function(o){return w(o.data,e,t)})},showSinglePoi:function(e,t,o,map,l,w){t.poiId=e;var P=map.getLayers().getArray().filter(function(t){return t.getProperties().id===e});P&&P.length&&map.removeLayer(P[0]);var _="",C=new r.a;return v.a.request({endPoint:"poi/".concat(e,"/?format=json")}).then(function(r){var v=(new c.a).readFeatures(r.data,{featureProjection:"EPSG:4326"});C.addFeatures(v);var P=Object(d.x)(C.getExtent());if(1===v.length){var x=v[0].getProperties(),I=x.geometry.getCoordinates();x.poiId=e,h.a.openIndrzPopup(t,null,e,"en",I,null,null,w,l,x,P,null,[0,-35]),m.a.zoomer(map.getView(),P,o),t.poiCatId=v[0].getProperties().category,t.poiCatShareUrl="?poi-cat-id="+v[0].getProperties().category;var k=new n.a({source:C,style:function(e,t){var o=e.getProperties().floor_name;_=e.getProperties().name||e.getProperties().name_en;var r=e.getProperties().category_icon_css_name;y.a.layerNamePrefix+o.toLowerCase()===w?e.setStyle(f.a.createPoiStyle(r,"y",o)):e.setStyle(f.a.createPoiStyle(r,"n",o))},title:_,name:_,id:e,active:!0,visible:!0,zIndex:999});return map.addLayer(k),k}})},setPoiFeatureVisibility:function(map,e){map.getLayers().forEach(function(t,i){t instanceof l.a&&("poi group"!==t.getProperties().name&&"POI-Gruppe"!==t.getProperties().name||t.getLayers().forEach(function(t,i){t.getSource().forEachFeature(function(t,i){y.a.layerNamePrefix+t.getProperties().floor_name.toLowerCase()!==e?t.setStyle(f.a.setPoiStyleOnLayerSwitch(t.getProperties().category_icon_css_name,!1)):t.setStyle(f.a.setPoiStyleOnLayerSwitch(t.getProperties().category_icon_css_name,!0))})}))})}}},415:function(e,t,o){"use strict";var r=o(358);o.n(r).a},416:function(e,t,o){(e.exports=o(11)(!1)).push([e.i,".poi{font-size:.875rem}.v-treeview-node__checkbox{display:none!important}",""])},417:function(e,t,o){"use strict";var r=o(359);o.n(r).a},418:function(e,t,o){(e.exports=o(11)(!1)).push([e.i,".floor-changer[data-v-6ba40e1f]{position:absolute;right:10px;top:70px;overflow-y:auto}",""])},435:function(e,t,o){var content=o(532);"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,o(12).default)("12082a03",content,!0,{sourceMap:!1})},438:function(e,t,o){var content=o(535);"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,o(12).default)("9aa5bc06",content,!0,{sourceMap:!1})},439:function(e,t,o){var content=o(539);"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,o(12).default)("0773dcba",content,!0,{sourceMap:!1})},451:function(e,t,o){"use strict";o(17);var r={name:"SnackBar",props:{timeout:{type:Number,default:function(){return 2e3}}},data:function(){return{show:!1,text:""}},created:function(){var e=this;this.$store.watch(function(e){return e.snackBar},function(){var t=e.$store.state.snackBar;""!==t&&(e.show=!0,e.text=t,e.$store.commit("SET_SNACKBAR",""))})}},n=o(32),c=o(36),l=o.n(c),d=o(145),f=o(600),component=Object(n.a)(r,function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("v-snackbar",{attrs:{timeout:e.timeout,top:!0},model:{value:e.show,callback:function(t){e.show=t},expression:"show"}},[e._v("\n  "+e._s(e.text)+"\n  "),o("v-btn",{attrs:{color:"blue",text:""},on:{click:function(t){e.show=!1}}},[e._v("\n    Close\n  ")])],1)},[],!1,null,"e4c8c062",null);t.a=component.exports;l()(component,{VBtn:d.a,VSnackbar:f.a})},453:function(e,t,o){"use strict";o(133),o(48),o(22),o(24);var r=o(131),n=o(78),c={props:{floors:{type:Array,default:function(){return[]}}},data:function(){return{setSelection:null}},watch:{floors:function(){this.setSelection&&this.selectFloorWithCss(this.setSelection)}},methods:{fetchFloors:function(){return r.a.request({endPoint:"floor/"})},onFloorClick:function(e,t){var o=n.a.layerNamePrefix+e.short_name.toLowerCase();this.$emit("floorClick",o),this.selectFloorWithCss(e.short_name.toLowerCase(),t)},selectFloorWithCss:function(e,t){var o=this;e.includes(n.a.layerNamePrefix)&&(e=e.split(n.a.layerNamePrefix)[1]),setTimeout(function(){var r=o.$el.querySelectorAll("[role=listitem]"),n=o.floors.findIndex(function(t){return t.short_name.toLowerCase()===e});r.forEach(function(e){e.classList.remove("v-list-item--active","v-list-item--link")}),r.length&&n>-1&&(r[n].classList.add("v-list-item--active","v-list-item--link"),t||r[n].scrollIntoView())},500)},getFloorByFloorName:function(e){var t=e.split(n.a.layerNamePrefix)[1];if(!t)return{};var o=this.floors.filter(function(e){return e.short_name.toLowerCase()===t});return o&&o.length?o[0]:{}}}},l=(o(417),o(32)),d=o(36),f=o.n(d),m=o(384),h=o(121),y=o(76),v=o(33),w=o(123),component=Object(l.a)(c,function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("v-card",{staticClass:"mx-auto floor-changer",attrs:{"max-height":"400px"}},[o("v-list",{attrs:{dense:""}},[o("v-list-item-group",{attrs:{mandatory:"",color:"primary"}},e._l(e.floors,function(t,i){return o("v-list-item",{key:i,on:{click:function(o){return o.stopPropagation(),e.onFloorClick(t,!0)}}},[o("v-list-item-content",{staticStyle:{"min-width":"20px"}},[o("v-list-item-title",{domProps:{textContent:e._s(t.short_name)}})],1)],1)}),1)],1)],1)},[],!1,null,"6ba40e1f",null);t.a=component.exports;f()(component,{VCard:m.a,VList:h.a,VListItem:y.a,VListItemContent:v.a,VListItemGroup:w.a,VListItemTitle:v.b})},454:function(e,t,o){"use strict";o(17),o(40);var r,n=o(13),c=o(152),l=o.n(c),d=o(131),f={name:"PointsOfInterest",props:{initialPoiCatId:{type:String,default:function(){return null}},initialPoiId:{type:String,default:function(){return null}},multi:{type:Boolean,default:function(){return!0}}},data:function(){return{files:{html:"mdi-language-html5",js:"mdi-nodejs",json:"mdi-json",md:"mdi-markdown",pdf:"mdi-file-pdf",png:"mdi-file-image",txt:"mdi-file-document-outline",xls:"mdi-file-excel"},tree:[],poiData:[],openedItems:[],forceReloadNode:!1,loading:!0,currentPoi:null}},watch:{tree:function(e,t){var o=[],r=[],n=[];!1===this.multi?(o=t,r=this.currentPoi):(t.length>e.length&&(o=l.a.differenceBy(t,e,"id")),e.length>t.length&&(r=l.a.differenceBy(e,t,"id")),n=l.a.intersectionBy(e,t,"id")),this.forceReloadNode&&e.length===t.length&&e[0].id===t[0].id&&(r=e,o=e,n=[],this.forceReloadNode=!1),this.$root.$emit("poiLoad",{newItems:r,oldItems:n,removedItems:o})}},mounted:function(){this.loadDataToPoiTree()},methods:{loadDataToPoiTree:(r=Object(n.a)(regeneratorRuntime.mark(function e(){var t,o,r=this;return regeneratorRuntime.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,this.fetchPoiTreeData();case 2:(t=e.sent)&&t.data&&(this.poiData=t.data,this.initialPoiCatId?(o=this.findItem(Number(this.initialPoiCatId),this.poiData),this.tree=[o.data],setTimeout(function(){var e=r.$refs.poi;e.updateSelected(r.initialPoiCatId,!0),o.roots.reverse().forEach(function(t){e.updateOpen(t,!0)}),e.updateActive(r.initialPoiCatId,!0)},500)):this.initialPoiId&&setTimeout(function(){r.$emit("loadSinglePoi",r.initialPoiId)},500)),this.loading=!1;case 5:case"end":return e.stop()}},e,this)})),function(){return r.apply(this,arguments)}),onTreeClick:function(e){var t=this.$refs.poi,o=!t.selectedCache.has(e.id);t.updateSelected(e.id,!1===this.multi||o),t.updateActive(e.id,!1===this.multi||o),this.currentPoi=e.children||[e],this.$emit("selectPoiCategory",e),t.emitSelected()},onLocationClick:function(e){this.$emit("locationClick",e.centroid)},fetchPoiTreeData:function(){return d.a.request({endPoint:"poi/tree/"})},findItem:function(e,data){var t=this,o=null;return data.some(function(r){return r.id&&r.id===e?(o=r,!0):r.children&&(o=t.findItem(e,r.children))?(o.roots?o.roots.push(r.id):o={data:o,roots:[r.id]},!0):void 0}),o}}},m=(o(415),o(32)),h=o(36),y=o.n(h),v=o(120),w=o(124),P=o(620),component=Object(m.a)(f,function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",[o("div",{staticClass:"text-center"},[e.loading?o("v-progress-circular",{attrs:{indeterminate:"",color:"primary"}}):e._e()],1),e._v(" "),e.loading?e._e():o("v-treeview",{ref:"poi",staticClass:"poi",attrs:{"multiple-active":e.multi,items:e.poiData,"selected-color":"indigo","open-on-click":"",selectable:"","return-object":"","item-key":"id",dense:""},scopedSlots:e._u([{key:"label",fn:function(t){var r=t.item;return[o("div",{staticStyle:{width:"100%",height:"100%"},on:{click:function(t){return e.onTreeClick(r)}}},[e._v("\n        "+e._s(r.name)+"\n      ")])]}},{key:"prepend",fn:function(t){var r=t.item,n=t.open,c=t.active;return[o("img",c?{attrs:{src:r.icon.replace(".","_active.")},on:{click:function(t){return e.onTreeClick(r)}}}:{attrs:{src:r.icon},on:{click:function(t){return e.onTreeClick(r)}}}),e._v(" "),r.icon?o("v-icon",[e._v("\n        mdi-"+e._s(r.icon)+"\n      ")]):o("v-icon",[e._v("\n        "+e._s(n?"mdi-folder-open":"mdi-folder")+"\n      ")])]}}],null,!1,3496622932),model:{value:e.tree,callback:function(t){e.tree=t},expression:"tree"}})],1)},[],!1,null,null,null);t.a=component.exports;y()(component,{VIcon:v.a,VProgressCircular:w.a,VTreeview:P.a})},531:function(e,t,o){"use strict";var r=o(435);o.n(r).a},532:function(e,t,o){(e.exports=o(11)(!1)).push([e.i,".indrz-zoom-control[data-v-c94eb222]{right:50px!important;bottom:100px!important;position:absolute}#id-map-switcher-widget[data-v-c94eb222]{position:absolute;right:45px!important;bottom:37px!important}",""])},534:function(e,t,o){"use strict";var r=o(438);o.n(r).a},535:function(e,t,o){(e.exports=o(11)(!1)).push([e.i,".speed-btn-panel[data-v-e5c4e8a8]{position:absolute;right:45px!important;bottom:70px!important}",""])},538:function(e,t,o){"use strict";var r=o(439);o.n(r).a},539:function(e,t,o){(e.exports=o(11)(!1)).push([e.i,".save-btn-panel[data-v-68af856d]{top:10px;position:absolute;left:calc(50% - 70px)}.poi[data-v-68af856d]{position:absolute;left:10px;top:70px;background:#fff;padding:15px;border-radius:5px}",""])},612:function(e,t,o){"use strict";o.r(t);o(65),o(66),o(3),o(40);var r,n,c=o(13),l=(o(77),o(25),o(454)),d=o(453),f=o(493),m=o(455),h=o(365),y=o(357),v=o(354),w=o(420),P=o(386),_=o(456),C=o(449),x=o(487),I=o(499),k=o(488),S=o(408),L=o(392),E=o(385),O=o(78),F=o(362),$=o(131),N=(o(433),{name:"Map",props:{selectedPoiCategory:{type:Object,default:function(){return null}},activeFloor:{type:Object,default:function(){return null}}},data:function(){return{mapId:"mapContainer",map:null,view:null,layers:[],isSatelliteMap:!0,vectorInteractionLayer:null,isAddPoiMode:!1,currentEditingPoi:null,modify:null,selectedPoi:null,deleteConfirm:!1}},mounted:(n=Object(c.a)(regeneratorRuntime.mark(function e(){return regeneratorRuntime.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,this.initializeMap();case 2:this.initializeEventHandlers();case 3:case"end":return e.stop()}},e,this)})),function(){return n.apply(this,arguments)}),methods:{initializeEventHandlers:function(){this.$root.$on("addPoiClick",this.addInteractions),this.$root.$on("deletePoiClick",this.confirmDeletePoi),this.$root.$on("cancelPoiClick",this.removeInteraction)},initializeMap:(r=Object(c.a)(regeneratorRuntime.mark(function e(){var t,o=this;return regeneratorRuntime.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return this.view=new m.a({center:F.a.getStartCenter(),zoom:17,maxZoom:23}),this.layers=F.a.getLayers(),this.map=new f.a({interactions:Object(C.a)().extend([new S.a,new L.a({constrainResolution:!0})]),target:this.mapId,controls:F.a.getMapControls(),view:this.view,layers:this.layers.layerGroups}),this.map.on("singleclick",this.onMapClick,this),window.onresize=function(){setTimeout(function(){o.map.updateSize()},500)},e.next=7,$.a.request({endPoint:"floor/"});case 7:(t=e.sent)&&t.data&&t.data.results&&(this.floors=t.data.results,this.floors&&this.floors.length&&(this.intitialFloor=this.floors.filter(function(e){return e.short_name.toLowerCase()===O.a.defaultStartFloor})[0],this.activeFloorName=O.a.layerNamePrefix+this.intitialFloor.short_name.toLowerCase(),this.$emit("floorChange",{floor:this.intitialFloor,floors:this.floors,name:this.activeFloorName}),this.wmsLayerInfo=F.a.getWmsLayers(this.floors)),this.layers.layerGroups.push(this.wmsLayerInfo.layerGroup),this.layers.switchableLayers=this.wmsLayerInfo.layers,this.map.addLayer(this.wmsLayerInfo.layerGroup));case 9:case"end":return e.stop()}},e,this)})),function(){return r.apply(this,arguments)}),onMapClick:function(e){var t=e.pixel,o=this.map.getFeaturesAtPixel(t),r=[];this.map.forEachFeatureAtPixel(t,function(e,t){r.push(e)});var n=(o=r[0])?o.getProperties():null;if(o){var c=o.getGeometry().getType().toString();"MultiPolygon"!==c&&"MultiPoint"!==c||"MultiPoint"===c&&(this.selectedPoi={featureId:o.getId(),categoryId:n.category})}},confirmDeletePoi:function(){this.selectedPoi&&this.selectedPoi.featureId?this.deleteConfirm=!0:this.$store.commit("SET_SNACKBAR","Please select the POI first to delete.")},onDeletePoiClick:function(){this.$root.$emit("deletePoi",this.selectedPoi),this.selectedPoi=null,this.deleteConfirm=!1},addInteractions:function(){this.selectedPoi=null,this.activeFloorName&&this.selectedPoiCategory?(this.isAddPoiMode=!0,this.source=new y.a,this.vectorInteractionLayer=new h.a({source:this.source,style:new v.c({fill:new w.a({color:"rgba(255, 255, 255, 0.2)"}),stroke:new P.a({color:"#ffcc33",width:2}),image:new _.a({radius:7,fill:new w.a({color:"#ffcc33"})})})}),this.modify=new x.a({source:this.source}),this.map.addInteraction(this.modify),this.map.addLayer(this.vectorInteractionLayer),this.draw=new I.a({source:this.source,type:"Point"}),this.map.addInteraction(this.draw),this.snap=new k.a({source:this.source}),this.map.addInteraction(this.snap),this.draw.on("drawend",this.onDrawEnd),this.modify.on("modifyend",this.onModifyEnd),this.modify.on("modifystart",this.onModifyStart)):this.$store.commit("SET_SNACKBAR","Please select the POI category and Active floor to continue")},onModifyStart:function(e){this.currentEditingPoi={oldCoord:e.target.dragSegments_[0][0].feature.getGeometry().getCoordinates()}},onModifyEnd:function(e){this.currentEditingPoi&&(this.currentEditingPoi.newCoord=e.target.dragSegments_[0][0].feature.getGeometry().getCoordinates(),this.$emit("updatePoiCoord",this.currentEditingPoi))},removeInteraction:function(){this.selectedPoi=null,this.isAddPoiMode=!1,this.map.removeInteraction(this.draw),this.map.removeInteraction(this.snap),this.map.removeLayer(this.vectorInteractionLayer),this.draw.un("drawend",this.onDrawEnd),this.modify.un("modifyend",this.onModifyEnd),this.modify.un("modifystart",this.onModifyStart)},onMapSwitchClick:function(){var e=this.layers.baseLayers;if(this.isSatelliteMap=!this.isSatelliteMap,this.isSatelliteMap)return e.ortho30cmBmapat.setVisible(!1),void e.greyBmapat.setVisible(!0);e.ortho30cmBmapat.setVisible(!0),e.greyBmapat.setVisible(!1)},onDrawEnd:function(e){if(this.isAddPoiMode){var t=e.feature.getGeometry().getCoordinates(),data={floor:1,name:this.selectedPoiCategory.name,description:"",enabled:!0,name_en:this.selectedPoiCategory.name_en,name_de:this.selectedPoiCategory.name_de,floor_num:this.activeFloor.floor_num,floor_name:this.activeFloor.short_name,category:this.selectedPoiCategory.id,geom:JSON.stringify({type:"MultiPoint",coordinates:[t],crs:{type:"name",properties:{name:"EPSG:3857"}}})};this.$emit("addnewPoi",data)}},onPoiLoad:function(e){var t=this,o=e.removedItems,r=e.newItems,n=e.oldItems;o&&o.length&&o.forEach(function(e){E.a.poiExist(e,t.map)&&E.a.removePoiById(e.id,t.map)}),n&&n.length&&n.forEach(function(e){E.a.setPoiVisibility(e,t.map)}),r&&r.length&&r.forEach(function(e){t.activeFloorName=O.a.layerNamePrefix+t.activeFloor.short_name.toLowerCase(),E.a.fetchPoi(e.id,t.map,t.activeFloorName).then(function(e){t.map.getLayers().forEach(function(t){99999===t.getProperties().id&&t.getLayers().push(e)})})})}}}),M=(o(531),o(32)),T=o(36),V=o.n(T),z=o(145),R=o(384),B=o(336),j=o(533),A=o(323),component=Object(M.a)(N,function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"fill-height"},[o("div",{ref:e.map,staticClass:"fill-height fluid flat width='100%' style='border-radius: 0",attrs:{id:e.mapId}}),e._v(" "),o("div",{staticClass:"indrz-zoom-control",attrs:{id:"zoom-control"}}),e._v(" "),o("div",{attrs:{id:"id-map-switcher-widget"}},[o("v-btn",{staticClass:"pa-2",attrs:{id:"id-map-switcher",color:"rgba(0,60,136,0.5)","min-width":"95px",small:"",dark:""},on:{click:e.onMapSwitchClick}},[e._v("\n      "+e._s(e.isSatelliteMap?"Satellite":"Map")+"\n    ")])],1),e._v(" "),e._m(0),e._v(" "),e._m(1),e._v(" "),o("v-dialog",{attrs:{persistent:"","max-width":"350"},model:{value:e.deleteConfirm,callback:function(t){e.deleteConfirm=t},expression:"deleteConfirm"}},[o("v-card",[o("v-card-title",[e._v("Are you sure you want to delete?")]),e._v(" "),o("v-card-actions",[o("v-spacer"),e._v(" "),o("v-btn",{attrs:{color:"error darken-1",text:""},on:{click:e.onDeletePoiClick}},[e._v("Yes")]),e._v(" "),o("v-btn",{attrs:{color:"blue darken-1",text:""},on:{click:function(t){e.deleteConfirm=!1}}},[e._v("Cancel")])],1)],1)],1)],1)},[function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"indrz-logo"},[t("a",{attrs:{href:"https://www.indrz.com",target:"_blank"}},[t("img",{attrs:{id:"indrz-logo",src:"/images/indrz-powered-by-90px.png",alt:"indrz logo"}})])])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"tu-logo"},[t("a",{attrs:{href:"https://www.tuwien.at",target:"_blank"}},[t("img",{staticStyle:{width:"auto",height:"40px"},attrs:{id:"tu-logo",src:"/images/tu-logo.png",alt:"tulogo"}})])])}],!1,null,"c94eb222",null),D=component.exports;V()(component,{VBtn:z.a,VCard:R.a,VCardActions:B.a,VCardTitle:B.c,VDialog:j.a,VSpacer:A.a});var U={name:"ActionButtons",data:function(){return{direction:"top",fab:!1,fling:!1,hover:!1,tabs:null,top:!1,right:!0,bottom:!0,left:!1,transition:"slide-y-reverse-transition"}},methods:{onAddPoiClick:function(){this.$root.$emit("addPoiClick")},onDeletePoiClick:function(){this.$root.$emit("deletePoiClick")}}},G=(o(534),o(120)),H=o(621),Y=Object(M.a)(U,function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"speed-btn-panel"},[o("v-speed-dial",{attrs:{top:e.top,bottom:e.bottom,right:e.right,left:e.left,direction:e.direction,"open-on-hover":e.hover,transition:e.transition},scopedSlots:e._u([{key:"activator",fn:function(){return[o("v-btn",{attrs:{color:"blue darken-2",dark:"",fab:""},model:{value:e.fab,callback:function(t){e.fab=t},expression:"fab"}},[e.fab?o("v-icon",[e._v("\n          mdi-close\n        ")]):o("v-icon",[e._v("\n          mdi-map-marker\n        ")])],1)]},proxy:!0}]),model:{value:e.fab,callback:function(t){e.fab=t},expression:"fab"}},[e._v(" "),o("v-btn",{attrs:{fab:"",dark:"",small:"",color:"green"}},[o("v-icon",[e._v("mdi-pencil")])],1),e._v(" "),o("v-btn",{attrs:{fab:"",dark:"",small:"",color:"indigo"},on:{click:function(t){return t.stopPropagation(),t.preventDefault(),e.onAddPoiClick(t)}}},[o("v-icon",[e._v("mdi-plus")])],1),e._v(" "),o("v-btn",{attrs:{fab:"",dark:"",small:"",color:"red"},on:{click:function(t){return t.stopPropagation(),t.preventDefault(),e.onDeletePoiClick(t)}}},[o("v-icon",[e._v("mdi-delete")])],1)],1)],1)},[],!1,null,"e5c4e8a8",null),X=Y.exports;V()(Y,{VBtn:z.a,VIcon:G.a,VSpeedDial:H.a});var W,J={name:"PoiManager",components:{PoiMap:D,ActionButtons:X,FloorChanger:d.a,PointsOfInterest:l.a},data:function(){return{activeFloor:null,activeFloorName:"",selectedPoiCategory:null,floors:[],newPoiCollection:[],initialPoiCatId:null}},mounted:function(){this.$root.$on("poiLoad",this.$refs.map.onPoiLoad),this.$root.$on("deletePoi",this.deletePoi)},methods:{setSelectedPoiCategory:function(e){this.selectedPoiCategory=e},onFloorClick:function(e){this.activeFloorName=e,this.activeFloor=this.$refs.floorChanger.getFloorByFloorName(e);var t=this.$refs.map,map=t.map,o=t.layers;F.a.activateLayer(this.activeFloorName,o.switchableLayers,map)},onMapFloorChange:function(e){var t=e.floor,o=e.floors,r=e.name;this.floors=o,this.activeFloor=t,this.$nextTick(function(){this.$refs.floorChanger.onFloorClick(t),this.activeFloorName=r})},onAddNewPoi:function(e){this.newPoiCollection.push(e)},onUpdatePoiCoord:function(e){var t=this.newPoiCollection.find(function(t){var o=JSON.parse(t.geom).coordinates[0];if(e.oldCoord[0]===o[0]&&e.oldCoord[1]===o[1])return t});t&&(t.geom=JSON.stringify({type:"MultiPoint",coordinates:[e.newCoord],crs:{type:"name",properties:{name:"EPSG:3857"}}}))},onSaveButtonClick:function(){var e=this;if(this.newPoiCollection.length){this.newPoiCollection.forEach(function(){var e=Object(c.a)(regeneratorRuntime.mark(function e(t){return regeneratorRuntime.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,$.a.postRequest({endPoint:"poi/",method:"POST",data:t});case 2:case"end":return e.stop()}},e)}));return function(t){return e.apply(this,arguments)}}());var t=this.$refs.poiTree;t.forceReloadNode=!0,this.initialPoiCatId=this.newPoiCollection[0].category.toString(),t.loadDataToPoiTree(),this.$refs.map.currentEditingPoi=null}this.$root.$emit("cancelPoiClick"),this.$nextTick(function(){e.newPoiCollection=[],e.$root.$emit("addPoiClick")})},deletePoi:(W=Object(c.a)(regeneratorRuntime.mark(function e(t){var o;return regeneratorRuntime.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,$.a.postRequest({endPoint:"poi/".concat(t.featureId),method:"DELETE",data:{}});case 2:(o=this.$refs.poiTree).forceReloadNode=!0,this.initialPoiCatId=t.categoryId.toString(),o.loadDataToPoiTree();case 6:case"end":return e.stop()}},e,this)})),function(e){return W.apply(this,arguments)}),onCancelButtonClick:function(){this.newPoiCollection=[],this.$root.$emit("cancelPoiClick")}}},K=(o(538),Object(M.a)(J,function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"fill-height"},[o("poi-map",{ref:"map",attrs:{"selected-poi-category":e.selectedPoiCategory,"active-floor":e.activeFloor},on:{floorChange:e.onMapFloorChange,addnewPoi:e.onAddNewPoi,updatePoiCoord:e.onUpdatePoiCoord}}),e._v(" "),o("div",{staticClass:"poi"},[o("points-of-interest",{ref:"poiTree",attrs:{multi:!1,"initial-poi-cat-id":e.initialPoiCatId},on:{selectPoiCategory:e.setSelectedPoiCategory}})],1),e._v(" "),o("div",{staticClass:"save-btn-panel"},[o("v-btn",{attrs:{color:"primary",small:"",width:"70px",disabled:!e.newPoiCollection.length},on:{click:function(t){return t.stopPropagation(),t.preventDefault(),e.onSaveButtonClick(t)}}},[e._v("\n      Save\n    ")]),e._v(" "),o("v-btn",{attrs:{color:"primary",small:"",width:"70px"},on:{click:function(t){return t.stopPropagation(),t.preventDefault(),e.onCancelButtonClick(t)}}},[e._v("\n      Cancel\n    ")])],1),e._v(" "),o("floor-changer",{ref:"floorChanger",attrs:{floors:e.floors},on:{floorClick:e.onFloorClick}}),e._v(" "),o("action-buttons")],1)},[],!1,null,"68af856d",null)),Z=K.exports;V()(K,{VBtn:z.a});var Q={layout:"admin",components:{PoiManager:Z,SnackBar:o(451).a}},ee=Object(M.a)(Q,function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"fill-height"},[t("poi-manager"),this._v(" "),t("snack-bar")],1)},[],!1,null,"0842737e",null);t.default=ee.exports}}]);