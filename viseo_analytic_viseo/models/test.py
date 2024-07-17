from odoo import api, fields, models

class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Model'

    name = fields.Char(string='Nom')
    value = fields.Integer(string='Valeur')

    @api.model
    def get_data(self):
        return self.search_read([])

class MyView(models.AbstractModel):
    _name = 'report.my_module.my_template'
    _description = 'My Template'

    @api.model
    def _get_report_values(self, docids, data=None):
        model_data = self.env['my.model'].get_data()
        return {
            'data': model_data
        }
