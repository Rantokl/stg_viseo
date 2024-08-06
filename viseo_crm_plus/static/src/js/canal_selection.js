odoo.define('your_module.canal_selection', function (require) {
    "use strict";

    var FieldSelection = require('web.relational_fields').FieldSelection;
    var FieldRegistry = require('web.field_registry');

    var SelectionWithPopup = FieldSelection.extend({
        events: _.extend({}, FieldSelection.prototype.events, {
            'change select': '_onSelectionChange',
        }),

        _onSelectionChange: function () {
            var self = this;
            var value = this.$el.find('select').val();
            this._setValue(value);

            if (value === 'social_media') {
                this._rpc({
                    model: this.model,
                    method: 'open_social_media_form',
                    args: [this.res_id],
                }).then(function(result) {
                    self.do_action(result);
                });
            }
        },
    });

    FieldRegistry.add('selection_with_popup', SelectionWithPopup);

    return SelectionWithPopup;
});