odoo.define('viseo_analytic_viseo.addchild', function(require) {
    "use strict";

    var rpc = require('web.rpc');
    var core = require('web.core');
    var ActionManager = require('web.ActionManager');

    $(document).ready(function() {

        $('#ajouterEnfantButton').on('click', function() {
            console.log('Test add child');
            rpc.query({
                model: 'ir.actions.act_window',
                method: 'search_read',
                args: [[['id', '=', 'action_child_wizard']]],
                fields: ['name', 'res_model', 'res_id', 'view_mode', 'view_id', 'target'],
            }).then(function(actions) {
                if (actions.length > 0) {
                    var action = actions[0];
                    var action_manager = new ActionManager();
                    action_manager.do_action(action);
                }
            });
        });
    });
});
