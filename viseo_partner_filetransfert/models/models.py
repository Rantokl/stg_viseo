# import xmlrpc.client
# from odoo import models, api

# class ResPartnerFileTransfer(models.Model):
#     _inherit = 'res.partner'
#
#     def transfer_file_to_remote(self, partner_id, file_content):
#         # Détails de la base de données distante
#         remote_url = "http://127.0.0.1:8520"
#         remote_db = "viseo13_data"
#         remote_username = "admin"
#         remote_password = "p@dm1n!123"
#
#         # Connexion à la base de données distante
#         remote_common = xmlrpc.client.ServerProxy(f"{remote_url}/xmlrpc/2/common")
#         remote_uid = remote_common.authenticate(remote_db, remote_username, remote_password, {})
#         remote_models = xmlrpc.client.ServerProxy(f"{remote_url}/xmlrpc/2/object")
#
#         # Récupération du partenaire dans la base distante
#         remote_partner = remote_models.execute_kw(
#             remote_db, remote_uid, remote_password, 'res.partner', 'search_read', [[('id', '=', partner_id)]], {'fields': ['cin_document_partner']}
#         )
#
#         # Mise à jour du fichier dans la base distante
#         if remote_partner:
#             remote_models.execute_kw(
#                 remote_db, remote_uid, remote_password, 'res.partner', 'write',
#                 [remote_partner[0]['id'], {'cin_document_partner': file_content}]
#             )
#             return True
#         else:
#             return False
#
#     def write(self, vals):
#         # Appel de la méthode write de base
#         result = super(ResPartnerFileTransfer, self).write(vals)
#
#         # Transférer le fichier après la sauvegarde
#         for partner in self:
#             file_content = vals['cin_document_partner']
#             if file_content:
#                 self.transfer_file_to_remote(3, file_content)
#                 print('//////////////////////////////////UPDTATE////////////////////////////////////' * 3)
#
#         return result
#     @api.model
#     def create(self, vals):
#         # Appel de la méthode write de base
#         result = super(ResPartnerFileTransfer, self).create(vals)
#
#         # # Transférer le fichier après la sauvegarde
#         # for partner in self:
#         #     file_content = vals.get('cin_document_partner')
#         #     if file_content:
#         #         self.transfer_file_to_remote(3, file_content)
#
#         print('//////////////////////////////////////////////////////////////////////'*3)
#         return result

import xmlrpc.client
from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def transfer_file_to_attachment_remote(self, partner_id, file_content, file_name):
        # Détails de la base de données distante
        remote_url = "http://127.0.0.1:8520"
        remote_db = "viseo13_data"
        remote_username = "admin"
        remote_password = "p@dm1n!123"

        # Connexion à la base de données distante
        remote_common = xmlrpc.client.ServerProxy(f"{remote_url}/xmlrpc/2/common")
        remote_uid = remote_common.authenticate(remote_db, remote_username, remote_password, {})
        remote_models = xmlrpc.client.ServerProxy(f"{remote_url}/xmlrpc/2/object")

        # Création de la pièce jointe dans la base distante
        attachment_data = {
            'name': file_name,
            'datas': file_content,
            'mimetype': 'application/octet-stream',  # Ajuster selon le type de fichier
            'res_model': 'res.partner',
            'res_id': partner_id,
        }

        # Créer la pièce jointe dans la base distante
        remote_models.execute_kw(
            remote_db, remote_uid, remote_password, 'ir.attachment', 'create',
            [attachment_data]
        )

    def write(self, vals):
        result = super(ResPartner, self).write(vals)

        # Transférer le fichier en tant que pièce jointe après la sauvegarde
        for partner in self:
            file_content = vals['cin_document_partner']  # Remplacez par le nom réel de votre champ fichier
            if file_content:
                # Encoder le contenu du fichier en base64 si nécessaire
                file_name = f"{vals['cin_document_partner_filename']},id={partner.id}" # Nom par défaut pour la pièce jointe
                self.transfer_file_to_attachment_remote(partner.id, file_content, file_name)

        return result
