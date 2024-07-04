from odoo import models, fields


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def _get_record_and_check(self, xmlid=None, model=None, id=None, field='datas', access_token=None):

# ===================================== PERMISSION D'APERCU DE DOCUMENT ============================================================
        # if self.sudo().env.user.ks_allow_preview:

        return super(IrHttp, self.sudo())._get_record_and_check(xmlid, model, id, field, access_token)
        # else:
        #     return super(IrHttp, self)._get_record_and_check(xmlid, model, id, field, access_token)
# ===================================================================================================================================


class Users(models.Model):
    _inherit = 'res.users'

    ks_allow_preview = fields.Boolean(string='Autorisaiton aperçu document',default=True ,help="Il permettra à l'utilisateur d'accéder à toutes les pièces jointes")
