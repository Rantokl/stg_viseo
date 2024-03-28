<!-- my_module/static/src/js/my_script.js -->
odoo.define('viseo_analytic_viseo.my_script', function (require) {
    'use strict';

    var core = require('web.core');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');

    var _t = core._t;
    var AbstractAction = require('web.AbstractAction');
    var MyFormView = Widget.extend({

        events: {
            'click button[name=action_afficher_template]': 'onAfficherTemplateClick',
        },

        onAfficherTemplateClick: function () {
            var self = this;
            console.log('Testtttt');
            this.rpc({
                model: 'viseo_analytic.viseo_analytic',
                method: 'action_afficher_templat',
                args: [this.res_id],
            }).then(function (result) {
                // Do something with the result if needed
                console.log('mety')
//                var data = [];
//                rpc.query({
//                    model: 'viseo_analytic.viseo_analytic',
//                    method: 'render_table',
//                    args: [1],
//                }).then(function(output) {
//                    data = output;
//                    console.log(output);
//                });
//            });
        },

        init: function(){
            this._super.apply(this, arguments);
            console.log('Analytic initialized....23');
        },

        start: function(){

            this.$el.empty();
            this.show_pivottt();
            return $.when();
        },

        show_pivottt: function(){
            console.log('Test 1234');
            var self = this;
            $(document).ready(function (){
                var data = [];
                rpc.query({
                    model: 'viseo_analytic.viseo_analytic',
                    method: 'render_table',
                    args: [1],
                }).then(function(output) {
                    data = output;
                    console.log(output);
                });
            }),
        },

//        readyTemplate: function(){
//            var self = this;
//            this._rpc({
//                model: 'viseo_analytic.viseo_analytic',
//                method: 'read_depart_group',
//                args: [this.res_id],
//            }).then(function (result) {
//                // Do something with the result if needed
//                console.log('Test ........');
//                console.log(this);
//            });
//        },
    });

    core.action_registry.add('mon_modele_form_view', MyFormView);

    return {
        MyFormView: MyFormView,
    };
});
