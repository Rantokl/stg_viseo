odoo.define('viseo_analytic_viseo.render_js', function(require){
    'use strict';

    var AbstractRenderer = require('web.AbstractRenderer');
    var FormView = require('web.FormView');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var analytic_view = FormView.extend({
        className : "mon_modele_form_view",
    init : function(){
        this._super.apply(this, arguments);
        console.log("View loaded.....");
    },
    _render: function () {
        this.$el.empty();
        this.show_pivottt();
        return $.when();
    },

    show_pivottt: function(){
        var self = this;
        console.log('Test')
        $('.container mt-5').css("height", "100%");
        $('.header').css("color","blue");
//        $('.container mt-5').append("<div id='container' style=' width: 100%;height: 100%;margin: 0;padding: 0;'></div>");
        anychart.onDocumentReady(function () {
            // create data
            console.log('Test')
            var data = [];
            rpc.query({
                model: 'viseo_analytic.viseo_analytic',
                method: 'render_table',
                args: [1],
            }).then(function(output) {
                data = output;
                console.log(output);
            });
        });
    },

    });

    core.action_registry.add('mon_modele_form_view', analytic_view);
    return {
        MyFormView: analytic_view,
    };


})