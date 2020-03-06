(window.webpackJsonp=window.webpackJsonp||[]).push([[8],{615:function(e,t,l){"use strict";l.r(t);l(10),l(9),l(4),l(7),l(3),l(191);var n=l(2),o=l(56),r=l(617),d=l(131),c={name:"AddEditShelf",props:{title:{type:String,default:function(){return""}},dialog:{type:Boolean,default:function(){return!1}},editedItem:{type:Object,default:function(){return{}}}},data:function(){return{loading:!1}},methods:{close:function(){this.$emit("close")},save:function(){var e=this;this.loading=!0,this.$store.dispatch("SAVE_SHELF",this.editedItem).then(function(t){e.$emit("save")}).catch(function(e){console.log(e)}).finally(function(){e.loading=!1})}}},m=l(32),f=l(36),v=l.n(f),h=l(145),_=l(384),x=l(335),I=l(603),y=l(321),S=l(535),O=l(516),k=l(120),V=l(600),w=l(323),j=l(497),component=Object(m.a)(c,function(){var e=this,t=e.$createElement,l=e._self._c||t;return l("v-dialog",{attrs:{value:e.dialog,persistent:"","max-width":"500px"}},[l("v-card",[l("v-card-title",[l("span",{staticClass:"headline"},[e._v(e._s(e.title))])]),e._v(" "),l("v-card-text",[l("v-form",[l("v-container",[l("v-row",{attrs:{"no-gutters":""}},[l("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[l("v-text-field",{attrs:{label:"External Shelf ID"},model:{value:e.editedItem.bookshelf_id,callback:function(t){e.$set(e.editedItem,"bookshelf_id",t)},expression:"editedItem.bookshelf_id"}})],1),e._v(" "),l("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[l("v-text-field",{attrs:{label:"Floor Number"},model:{value:e.editedItem.floor,callback:function(t){e.$set(e.editedItem,"floor",t)},expression:"editedItem.floor"}})],1),e._v(" "),l("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[l("v-text-field",{attrs:{label:"External Shelf Section"},model:{value:e.editedItem.external_id,callback:function(t){e.$set(e.editedItem,"external_id",t)},expression:"editedItem.external_id"}})],1),e._v(" "),l("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[l("v-text-field",{attrs:{label:"Shelving System End Value"},model:{value:e.editedItem.system_to,callback:function(t){e.$set(e.editedItem,"system_to",t)},expression:"editedItem.system_to"}})],1),e._v(" "),l("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[l("v-text-field",{attrs:{label:"Shelving System Start Value"},model:{value:e.editedItem.system_from,callback:function(t){e.$set(e.editedItem,"system_from",t)},expression:"editedItem.system_from"}})],1),e._v(" "),l("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[l("v-text-field",{attrs:{label:"Left or Right Side"},model:{value:e.editedItem.side,callback:function(t){e.$set(e.editedItem,"side",t)},expression:"editedItem.side"}})],1),e._v(" "),l("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[l("v-text-field",{attrs:{label:"Distance From Measure"},model:{value:e.editedItem.measure_from,callback:function(t){e.$set(e.editedItem,"measure_from",t)},expression:"editedItem.measure_from"}})],1),e._v(" "),l("v-col",{attrs:{cols:"12",sm:"12",md:"12"}},[l("v-text-field",{attrs:{label:"Distance End Measure"},model:{value:e.editedItem.measure_to,callback:function(t){e.$set(e.editedItem,"measure_to",t)},expression:"editedItem.measure_to"}})],1)],1)],1)],1)],1),e._v(" "),l("v-card-actions",[l("v-spacer"),e._v(" "),l("v-btn",{attrs:{color:"blue darken-1",text:"",disabled:e.loading},on:{click:e.close}},[e._v("\n        Cancel\n      ")]),e._v(" "),l("v-btn",{attrs:{color:"blue darken-1",text:"",loading:e.loading,disabled:e.loading},on:{click:e.save}},[e._v("\n        Save\n        "),l("v-icon",{attrs:{right:""}},[e._v("\n          mdi-save\n        ")])],1)],1)],1)],1)},[],!1,null,"bd826d88",null),D=component.exports;v()(component,{VBtn:h.a,VCard:_.a,VCardActions:x.a,VCardText:x.b,VCardTitle:x.c,VCol:I.a,VContainer:y.a,VDialog:S.a,VForm:O.a,VIcon:k.a,VRow:V.a,VSpacer:w.a,VTextField:j.a});var filter=l(604),E=l(619),$=l(605);function L(object,e){var t=Object.keys(object);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(object);e&&(l=l.filter(function(e){return Object.getOwnPropertyDescriptor(object,e).enumerable})),t.push.apply(t,l)}return t}var C={name:"ShelvesList",components:{AddEditShelf:D},data:function(){return{loading:!1,singleSelect:!1,dialog:!1,selected:[],pagination:{},search:"",term$:new r.a,headers:[{text:"External Id",align:"right",sortable:!1,value:"external_id"},{text:"Floor",align:"right",filterable:!1,sortable:!1,value:"floor"},{text:"System From",align:"right",sortable:!0,value:"system_from"},{text:"System To",align:"right",sortable:!0,value:"system_to"},{text:"Shelf Side",align:"right",filterable:!1,sortable:!1,value:"side"},{text:"Measure From",align:"right",filterable:!1,sortable:!1,value:"measure_from"},{text:"Measure To",align:"right",filterable:!1,sortable:!1,value:"measure_to"},{text:"Map",value:"map",sortable:!1,filterable:!1,width:"56px"},{text:"Edit",value:"edit",sortable:!1,filterable:!1,width:"56px"}],editedIndex:-1,editedItem:{},defaultItem:{bookshelf_id:null,external_id:null,floor:null,id:null,measure_from:null,measure_to:null,section_child:null,section_id:null,section_main:null,side:"L",system_from:null,system_to:null}}},computed:function(e){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?L(source,!0).forEach(function(t){Object(n.a)(e,t,source[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(source)):L(source).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(source,t))})}return e}({},Object(o.c)({shelvesListData:function(e){var t=e.user.shelves,data=t.data,l=t.total;return this.total=l,data}}),{formTitle:function(){return-1===this.editedIndex?"New Shelf":"Edit Shelf"}}),watch:{search:function(text){this.term$.next(text)},dialog:function(e){e||this.close()},pagination:{handler:function(){this.loadData()},deep:!0}},mounted:function(){var e=this;this.term$.pipe(Object(filter.a)(function(e){return!e||e.length>2}),Object(E.a)(500),Object($.a)()).subscribe(function(t){return e.loadData(t)}),this.loadData()},methods:{loadData:function(e){var t=this;if(!this.loading){this.loading=!0;var l=d.a.getPageParams(this.pagination);e&&(l.search=e),this.$store.dispatch("user/LOAD_SHELVES",l).catch(function(e){console.log(e)}).finally(function(){t.loading=!1})}},editItem:function(e){this.editedIndex=this.shelvesListData.indexOf(e),this.editedItem=Object.assign({},e),this.dialog=!0},close:function(){var e=this;this.dialog=!1,setTimeout(function(){e.editedItem=Object.assign({},e.defaultItem),e.editedIndex=-1},300)},save:function(){this.editedIndex>-1&&Object.assign(this.shelvesListData[this.editedIndex],this.editedItem),this.close()}}},P=l(616),T=Object(m.a)(C,function(){var e=this,t=e.$createElement,l=e._self._c||t;return l("div",[l("v-card",[l("v-card-title",[e._v("\n      Regal\n      "),l("v-spacer"),e._v(" "),l("v-text-field",{attrs:{label:"Search",clearable:"","single-line":"","hide-details":""},model:{value:e.search,callback:function(t){e.search=t},expression:"search"}})],1),e._v(" "),l("v-data-table",{staticClass:"elevation-1",attrs:{headers:e.headers,items:e.shelvesListData,"server-items-length":e.total,"single-select":e.singleSelect,"item-key":"id",options:e.pagination,"show-select":"",loading:e.loading,"loading-text":"Loading... Please wait"},on:{"update:options":function(t){e.pagination=t}},scopedSlots:e._u([{key:"top",fn:function(){return[l("add-edit-shelf",{attrs:{title:e.formTitle,dialog:e.dialog,"edited-item":e.editedItem},on:{save:e.save,close:e.close}})]},proxy:!0},{key:"item.map",fn:function(t){t.item;return[l("v-icon",{attrs:{small:""}},[e._v("\n          mdi-map\n        ")])]}},{key:"item.edit",fn:function(t){var n=t.item;return[l("v-icon",{attrs:{small:""},on:{click:function(t){return e.editItem(n)}}},[e._v("\n          mdi-pencil\n        ")])]}}]),model:{value:e.selected,callback:function(t){e.selected=t},expression:"selected"}})],1)],1)},[],!1,null,"25e0f370",null),F=T.exports;v()(T,{VCard:_.a,VCardTitle:x.c,VDataTable:P.a,VIcon:k.a,VSpacer:w.a,VTextField:j.a});var A={layout:"admin",components:{ShelvesList:F}},M=Object(m.a)(A,function(){var e=this.$createElement,t=this._self._c||e;return t("div",[t("shelves-list")],1)},[],!1,null,"097ab972",null);t.default=M.exports}}]);