// your_module/static/src/js/custom_widget.js
odoo.define('viseo_analytic_viseo.template', function (require) {
    "use strict";

     var FieldHtml = require('web.basic_fields').FieldHtml;
    var fieldRegistry = require('web.field_registry');

    var CustomHtmlWidget = FieldHtml.extend({
        template: 'your_module.custom_html_template_analytique',
    });

    fieldRegistry.add('custom_html_widget', CustomHtmlWidget);

    return CustomHtmlWidget;
});
