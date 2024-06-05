odoo.define('viseo_whatsapp.custom_Chatter', function (require) {
    "use strict";

    var Chatter = require('mail.Chatter');
    var rpc = require('web.rpc');

    Chatter.include({
        start: function () {
            this._super.apply(this, arguments);
            this.$('.o_chatter_button_whatsapp').click(this._onCustomButtonClick.bind(this));
        },
        _onCustomButtonClick: function (ev) {

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
                                 'default_group_name':output['name']
                                 },
                       target: 'new',
                        });
                    });

        }
    });

});
