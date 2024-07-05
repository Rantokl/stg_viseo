odoo.define('viseo_analytic_viseo.ecriture', function (require) {
    "use strict";
    var rpc = require('web.rpc');
    var FormController = require('web.FormController');

    FormController.include({
        events: {
            'click .cell-header': 'onAfficherWizard',
            'click .cell-body': 'onAfficherWizard',
//            "click button[name='table_analytic']": "table_analytic",
//            'click #ajouterEnfantButton': 'openAddchild',
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

    });


});