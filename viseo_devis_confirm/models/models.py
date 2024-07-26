from odoo import models, fields, api, exceptions
from datetime import datetime, time 

class viseo_devis_confirm(models.Model):
    _inherit = 'sale.order'

    def doc_empty_alert(self, vals):
        raise exceptions.UserError(f"Ajoutez le '{vals}' de '{self.partner_id.name}' dans la fiche contact")
    
    def action_confirm(self):
        if self.partner_id.company_type == "person":
            now_datetime_start = datetime.combine(datetime.now().date(), time.min)
            now_datetime_stop = datetime.combine(datetime.now().date(), time.max)
            domain = [('partner_id', '=', self.partner_id.id),('create_date', '>=', now_datetime_start),('create_date', '<=', now_datetime_stop)]
            sale_exist = self.env['sale.order'].search(domain).read(['create_date'])
            
            if self.amount_total > 10000000:
                if not self.partner_id.cin_document_partner:
                    self.doc_empty_alert("CIN")
            if len(sale_exist)>2:
                if not self.partner_id.cin_document_partner:
                    self.doc_empty_alert("CIN")
        return super(viseo_devis_confirm, self).action_confirm()
