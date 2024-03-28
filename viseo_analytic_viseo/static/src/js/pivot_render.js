odoo.define('viseo_analytic_viseo.pivot_render', function (require) {
    "use strict";

    // console.log("Module loaded")
   
    var core = require('web.core');
    var AbstractRenderer = require('web.AbstractRenderer');
    var rpc = require('web.rpc');
   var analytic_view = AbstractRenderer.extend({
    className : "pivot_table",
    init : function(){
        this._super.apply(this, arguments);
        console.log("View loaded2");
    },
    _render: function () {
        this.$el.empty();
        this.show_pivottt();
        return $.when();
    },

    show_pivottt: function(){
        var self = this;	
        $('.pivot_table').css("height", "100%");	
        $('.pivot_table').append("<div id='container' style=' width: 100%;height: 100%;margin: 0;padding: 0;'></div>");
        anychart.onDocumentReady(function () {    
            // create data
            var data = [];
            rpc.query({
                model: 'viseo_analytic.viseo_analytic',
                method: 'read_group_department_ids',
                args: [1],
            }).then(function(output) {
                data = output;
                console.log(output);
            });
        });
    },
})
    
return analytic_view
});