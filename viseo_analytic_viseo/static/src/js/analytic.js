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
            'click #ajouterEnfantButton': 'openAddchild',
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
            this._super.apply(this, arguments);
        },

        openAddchild : function(ev){
            ev.preventDefault();
            rpc.query({
                 model: 'analytic.addchild',
                 method: 'openWizardChild',
                 args: [[]],
            }).then(function(output){
                   console.log('Open wizard')
//                   self.do_action({
//
//                       name: 'Whatsapp',
//                       type: 'ir.actions.act_window',
//                       res_model: 'analytic.addchild',
//                       view_mode: 'form',
//                       views: [[false, 'form']],
////                       context:{'default_id_model':idValue,
////                                 'default_model_name': modelValue,
//////                                 'default_group_name':output['name']
////                                 },
//                       target: 'new',
//                        });

            });
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
                var value_id = parseInt(idValue)
                console.log(value_id);
                rpc.query({
                    model: 'viseo_analytic.viseo_analytic',
                    method: 'render_table',
                    args: [value_id],
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
                    model: 'viseo_analytic.viseo_analytic',
                    method: 'calcul_value_rebrique',
                    args: [value_id],
                    }).then(function(output){
                        console.log(typeof(output['famille']))
                        const table = document.querySelector("#tableanalytique");

                        const body = table.querySelector("tbody");
                        body.className = 'cell-body'
                        for (var i = 0; i < output['famille'].length; i++) {
                            var ligne = table.insertRow(i + 1);
                            for (var j = 0; j < output['famille'][i].length; j++) {
                                var cellule = ligne.insertCell(j);
                                // Si la colonne est >= 1 et contient des valeurs numériques, appliquez le format Ariary
                                if (j >= 1 && typeof output['famille'][i][j] === 'number') {
                                    cellule.innerHTML = output['famille'][i][j].toLocaleString('en-MG', { style: 'currency', currency: 'MGA' });
                                    cellule.className = 'currency';
                                } else {
                                    cellule.innerHTML = output['famille'][i][j];
                                }
                            }
                        }
//


                    }),

                    rpc.query({
                        model: 'viseo_analytic.viseo_analytic',
                        method: 'table_analytic',
                        args:[[]],
                    }).then(function(result){
                        console.log('idValue:',idValue)
                        console.log(result)
                        rpc.query({
                        model: 'viseo_analytic.viseo_analytic',
                        method: 'takedata',
                        args:[value_id],
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