odoo.define('viseo_analytic_viseo.custom_template', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    init: function(){
            this._super.apply(this, arguments);
            console.log('Analytic initialized....');
        },
        _render: function () {

            this.$el.empty();

            return $.when();
        },

        start: function(){
//            this.show_pivott()
            this._super.apply(this, arguments);
        },

//    publicWidget.registry.CustomTemplate = publicWidget.Widget.extend({
//        selector: '.pivot_table',
//        start: function () {
//            this._super.apply(this, arguments);
//            this.setHeaderValues();
//        },
//        setHeaderValues: function () {
//            document.getElementById('header1').innerText = 'Nouvelle Valeur';
//            // Add more JavaScript to dynamically set values as needed
//        }
//    });
});
