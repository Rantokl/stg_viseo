odoo.define('viseo_whatsapp.ChatterViseo', function (require) {
"use strict";

//var Activity = require('mail.Activity');
//var AttachmentBox = require('mail.AttachmentBox');
//var ChatterComposer = require('mail.composer.Chatter');
//var Dialog = require('web.Dialog');
//var Followers = require('mail.Followers');
//var ThreadField = require('mail.ThreadField');
//var mailUtils = require('mail.utils');
//
//var concurrency = require('web.concurrency');
//var config = require('web.config');
//var core = require('web.core');
//var Widget = require('web.Widget');
//
//var _t = core._t;
//var QWeb = core.qweb;

// The purpose of this widget is to display the chatter area below the form view
//
// It instantiates the optional mail_thread, mail_activity and mail_followers widgets.
// It Ensures that those widgets are appended at the right place, and allows them to communicate
// with each other.
// It synchronizes the rendering of those widgets (as they may be asynchronous), to mitigate
// the flickering when switching between records
var KanbanColumn = require("mail.Chatter");
     var rpc = require('web.rpc');

    KanbanColumn.include({

        events: {
        'click .o_chatter_button_whatsapp': '_openWhatsapp',

        },
        /**
        * Discard changes on the record.
        * This is notified by the composer, when opening the full-composer.
        * @private
        * @param {OdooEvent} ev
        * @param {function} ev.data.proceed callback to tell to proceed
        */
        _getParamValue : function(url, paramName) {
            var params = url.split('&');
            for (var i = 0; i < params.length; i++) {
                var param = params[i].split('=');
                if (param[0] === paramName) {
                    return decodeURIComponent(param[1]);
                }
            }
            return null;
        },

        _openWhatsapp : function(ev){
           var self=this;
           var url = window.location.href;
           var params = url.split('#').join('&');

           params = params.split('&');
           for (var i = 0; i < params.length; i++) {
                var param = params[i].split('=');
                if (param[0] === 'id') {
                    var idValue = decodeURIComponent(param[1]);
                }else{
                    if (param[0] === 'model') {
                    var modelValue = decodeURIComponent(param[1]);
                }
            }
            }


            ev.preventDefault();


            rpc.query({
                    model: 'whatsapp.viseo',
                    method: 'take_group_whatsapp',
                    args: [[],modelValue, idValue],
                    }).then(function(output){
                        self.do_action({

                       name: 'Whatsapp',
                       type: 'ir.actions.act_window',
                       res_model: 'whatsapp.viseo',
                       view_mode: 'form',
                       views: [[false, 'form']],
                       context:{'default_id_model':idValue,
                                 'default_model_name': modelValue,
//                                 'default_group_name':output['name']
                                 },
                       target: 'new',
                        });
                    });

        },
    });


//return KanbanColumn;

});
