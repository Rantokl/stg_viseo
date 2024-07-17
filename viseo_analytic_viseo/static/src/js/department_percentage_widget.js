
// static/src/js/department_percentage_widget.js
odoo.define('viseo_analytic_viseo.department_percentage_widget', function (require) {
    "use strict";

    var FieldText = require('web.basic_fields').FieldText;
    var registry = require('web.field_registry');
    var core = require('web.core');
    var QWeb = core.qweb;

    var DepartmentPercentageWidget = FieldText.extend({
        template: 'DepartmentPercentageWidget',

        events: _.extend({}, FieldText.prototype.events, {
            'click .add-row': '_onAddRow',
            'click .remove-row': '_onRemoveRow',
            'input .department-input': '_onInputChange',
        }),

        start: function () {
            this._super.apply(this, arguments);
            this._renderTable();
        },

        _renderTable: function () {
            var table_data = JSON.parse(this.value || '[]');
            var department_names = this.recordData.department_names.split(',');
            var total_people = this.recordData.department_totals || 0;
            var $table = this.$('.department-percentage-table');
            $table.empty();

            // Add table header
            var $header = $('<tr>');
            $header.append($('<th>').text('Department'));
            $header.append($('<th>').text('Number of People'));
            $header.append($('<th>').text('Percentage'));
            $table.append($header);

            // Add table rows
            for (var i = 0; i < department_names.length; i++) {
                var $row = $('<tr>');
                $row.append($('<td>').text(department_names[i]));
                var number_of_people = table_data[i] ? table_data[i][0] : 0;
                var percentage = total_people ? ((number_of_people / total_people) * 100).toFixed(2) : 0;
                $row.append($('<td>').append($('<input type="number" class="department-input" data-index="'+i+'" value="'+number_of_people+'">')));
                $row.append($('<td>').append($('<span class="percentage-value">'+percentage+'%</span>')));
                $table.append($row);
            }
        },

        _onAddRow: function () {
            var department_names = this.recordData.department_names.split(',');
            var $table = this.$('.department-percentage-table');
            var $row = $('<tr>');
            $row.append($('<td>').append($('<input type="text">')));
            $row.append($('<td>').append($('<input type="number" class="department-input">')));
            $row.append($('<td>').append($('<span class="percentage-value">0%</span>')));
            $table.append($row);
        },

        _onRemoveRow: function (event) {
            $(event.currentTarget).closest('tr').remove();
        },

        _onInputChange: function () {
            var total_people = parseInt(this.recordData.department_totals) || 0;
            var table_data = [];
            this.$('.department-percentage-table tr').each(function (index, row) {
                if (index > 0) { // Skip header row
                    var inputs = $(row).find('input');
                    var number_of_people = parseInt(inputs.eq(1).val()) || 0;
                    table_data.push([number_of_people]);
                }
            });

            this.value = JSON.stringify(table_data);
            this._renderTable();
        },

        _onSave: function () {
            var table_data = [];
            this.$('.department-percentage-table tr').each(function () {
                var row = [];
                $(this).find('td input').each(function () {
                    row.push($(this).val());
                });
                if (row.length > 0) {
                    table_data.push(row);
                }
            });
            this._setValue(JSON.stringify(table_data));
        },
    });

    registry.add('department_percentage_table', DepartmentPercentageWidget);
    return DepartmentPercentageWidget;
});