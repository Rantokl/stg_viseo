from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

#champ avec responsable assigné par défaut et envoi automatique de notification
class ImportFollowup(models.Model):
    _inherit= 'import.followup'

    #domaine pour récupérer les membres du groupe 'Mon Groupe'
    def _domain_assigned_users(self):
        return [('groups_id', 'in', [self.env.ref('groupe.group_my_group').id])]

    #prendre un seul utilisateur par défaut
    def _default_assigned_users(self):
        group_my_group = self.env.ref('groupe.group_my_group')
        default_user = group_my_group.users[:1]  # Prendre le premier utilisateur du groupe
        return [(4, default_user.id)] if default_user else False

    #valeur du champ assigned users
    assigned_users_ids = fields.Many2many(
        'res.users',
        string='Utilisateurs Assignés',
        domain=_domain_assigned_users,
        help='Select users for assignment',
        groups='groupe.group_my_group',
        default=_default_assigned_users,
        required=True,
        readonly=False
    )

    def send_notification_to_assigned_users(self, user):
        message = "You have been assigned to a new import follow-up."
        self.message_post(body=message, partner_ids=user.partner_id.ids)
        _logger.info("Notification sent to user %s: %s", user.name, message)

    #assignation dès l'utilisateur assigné par défaut
    @api.model
    def create(self, vals):
        res = super(ImportFollowup, self).create(vals)
        if res.assigned_users_ids:
            for user in res.assigned_users_ids:
                res.send_notification_to_assigned_users(user)
        return res

    def write(self, vals):
        res = super(ImportFollowup, self).write(vals)
        if 'assigned_users_ids' in vals:
            new_assigned_users = self.env['res.users'].browse(vals['assigned_users_ids'][0][2])
            for user in new_assigned_users:
                self.send_notification_to_assigned_users(user)
        return res




    
 
    

