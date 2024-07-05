odoo.define('viseo_analytic_viseo.custom_template', function (require) {
    "use strict";


   var rpc = require('web.rpc');
    var FormController = require('web.FormController');
    var rpc = require('web.rpc');
    var isShowPivottExecuted = false;

    FormController.include({
        events: {
            'click .cell-header': 'onAfficherWizard',
            'click .cell-body': 'onAfficherWizard',
//            "click button[name='table_analytic']": "table_analytic",
//            'click #ajouterEnfantButton': 'openAddchild',
        },

//        $(document).ready(function () {
//            this.show_pivott();
//        }),

//        init: function(){
//            this._super.apply(this, arguments);
//
//            console.log('Analytic initialized....');
//            this.hasShownPivott = false;
//        },
        start: function(){
//            this.show_pivott();
//            console.log(this.hasShownPivott)
            this._super.apply(this, arguments);
            if (this.modelName === 'viseo.analytique.view') {
                this.show_pivott();
                isShowPivottExecuted = true; // Marquer show_pivott() comme déjà exécuté
            }
//            if (this.hasShownPivott==false) {
//                this.show_pivott();
//                console.log(!this.hasShownPivott)
//                this.hasShownPivott = true;  // Marquer show_pivott() comme déjà exécuté
//            }else{
//                console.log(this.hasShownPivott)
//            }
        },



         show_pivott: function(){

            var self = this;

//            $(document).ready(function () {

                var data = [];
                var url = window.location.href;
                var params = url.split('#').join('&');
                params = params.split('&');
                var idValue = null;
                var modelValue = null;
                var activeIdValue = null;
//
//
//
//                // Parcours des paramètres et récupération des valeurs
                for (var i = 0; i < params.length; i++) {
                    var param = params[i].split('=');
                    var paramName = param[0];
                    var paramValue = decodeURIComponent(param[1]);

                    if (paramName === 'active_id') {
                        activeIdValue = paramValue;
                    } else if (paramName === 'id') {
                        idValue = paramValue;
//                    } else if (paramName === 'model') {
//                        modelValue = paramValue;
//                    }
                }
                }
//
//                console.log('Active ID value:', activeIdValue);
//                console.log('ID value:', idValue);
//                console.log('Model value:', modelValue);

//                console.log('id : ',idValue);

                rpc.query({
                    model: 'viseo_analytic.viseo_analytic',
                    method: 'action_afficher_template',
                    args: [[]],
                    }).then(function(output){
                        console.log(output)
                        const table = document.querySelector("#tableanalytique");

//                        if (output['model'] == 'viseo.analytique.view'){
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
//                        console.log('idValue:',idValue)
//                        console.log(result)
                        rpc.query({
                        model: 'viseo_analytic.viseo_analytic',
                        method: 'takedata',
                        args:[value_id],
                    }).then(function(output){
                        console.log('Test',output)
//                        var element = document.getElementById('name');
//
//                        element.appendChild(document.createTextNode(output['name']));
                    })

                    })
//                }

                    });



//                });

                },
                onAfficherWizard : function(){
//            ev.preventDefault();
            var self = this;

                rpc.query({
                        model: 'viseo_analytic.viseo_analytic',
                        method: 'openWizard',
                        args:[[]],
                    }).then(function(result){
                        console.log('Wizard')
                        self.do_action({

                       name: 'Ecriture',
                       type: 'ir.actions.act_window',
                       res_model: 'account.move.line.view',
                       view_mode: 'form',
                       views: [[false, 'form']],
                       context:{
                                 },
                       target: 'new',
                        });
                    });



        },


//         },


    });
});
