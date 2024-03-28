odoo.define('viseo_analytic_viseo.analytic', function (require) {
    "use strict";

    console.log("Module loaded")
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var AbstractRenderer = require('web.AbstractRenderer');
    var Analytic = AbstractAction.extend({
        template:'custom_html_template',

        events: {
            'click .cell-header': 'onAfficherWizard',
            'click .cell-body': 'onAfficherWizard',
            "click button[name='table_analytic']": "table_analytic",
        },

        init: function(){
            this._super.apply(this, arguments);
            console.log('Analytic initialized....');
        },
        _render: function () {

            this.$el.empty();

            return $.when();
        },

        start: function(){
            this.show_pivott()
        },

        table_analytic : function(){
            console.log('Test gfkg')
        },

        onAfficherWizard : function(){
            rpc.query({
                 model: 'viseo_analytic.viseo_analytic',
                 method: 'openWizard',
                 args: [1],
            }).then(function(output){

                showModal('Content')
            })
        },
    
        show_pivott: function(){

            var self = this;

            $(document).ready(function () {

                var data = [];
                var url = window.location.href;
                var params = url.split('#').join('&');
                params = params.split('&');
                for (var i = 0; i < params.length; i++) {
                   var param = params[i].split('=');
                   if (param[0] === 'active_id') {
                      var idValue = decodeURIComponent(param[1]);
                        }
                   }

                console.log('id : ',idValue);
                rpc.query({
                    model: 'viseo_analytic.viseo_analytic',
                    method: 'render_table',
                    args: [1],
                    }).then(function(output) {
                    const table = document.querySelector("#tableanalytique");
                    const headers = table.querySelector("thead tr");
                    const body = table.querySelector("tbody");
                    const modal = document.querySelector(".cell-header");
                    for (var i in output['departements']){
                        var val = output['departements'][i]

                        const header = document.createElement("th");

                        header.className = 'cell-header'
                        header.innerText = val;
                        headers.append(header);
//                        $(document).getElementById('buttonLED'+id).onclick = function(){ writeLED(1,1); }
//                        modal.onclick = function modals(){showModal(val);}

                    }
                }),

                rpc.query({
                    model: 'famille.analytique',
                    method: 'calcul_value_rebrique',
                    args: [1],
                    }).then(function(output){
                        console.log(output['famille'])
                        const table = document.querySelector("#tableanalytique");

                        const body = table.querySelector("tbody");
                        body.className = 'cell-body'
                        for (var i = 0; i < output['famille'].length; i++) {
                            var ligne = table.insertRow(i + 1);
                            for (var j = 0; j < output['famille'][i].length; j++) {
                                var cellule = ligne.insertCell(j);
                                cellule.innerHTML = output['famille'][i][j];
                            }
                        }

                    }),

                    rpc.query({
                        model: 'viseo_analytic.viseo_analytic',
                        method: 'table_analytic',
                        args:[1],
                    }).then(function(result){
                        console.log('idValue:',idValue)
                        console.log(result)
                        rpc.query({
                        model: 'viseo_analytic.viseo_analytic',
                        method: 'takedata',
                        args:[idValue],
                    }).then(function(output){
                        console.log('Test',output)
                        var element = document.getElementById('name');

                        element.appendChild(document.createTextNode(output['name']));
                    })

                    })

                });

                },


            });

   



   core.action_registry.add('viseo_analytic_viseo',Analytic);
   return Analytic;
});