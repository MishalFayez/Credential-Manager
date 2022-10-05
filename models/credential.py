import string
import random
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from pathlib import Path
import cryptocode


def get_key():
    cm_directory = Path(__file__).absolute().parent.parent
    with open(cm_directory / 'key/k.txt', 'r') as k:
        key = k.readline()
    return key


class CredentialManager(models.Model):
    _name = "credential.manager"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Credential Manager"

    name = fields.Char(string='Name', required=True, tracking=True)
    urls = fields.Char(string="URL", tracking=True)
    email = fields.Char(string='Username', required=True, tracking=True)
    passwords = fields.Char(string='Password', tracking=True, required=True)
    note = fields.Text(string='note', tracking=True)
    partner_ids = fields.Many2many('res.users', string='Followers', tracking=True)
    show_password = fields.Boolean(string='Show Password')
    password_no_stars = fields.Char(string='Real Password', compute='_get_password')

    def _get_password(self):
        self.password_no_stars = cryptocode.decrypt(self.passwords,get_key())
    @api.model
    def create(self, vals):
        # characters = list(string.ascii_letters + "!@#$")
        # password = ''
        # for i in range(4):
        #     password += random.choice(characters)
        # if not vals.get('passwords'):
        #     vals['passwords'] = password
        # print(vals.get('partner_ids')[0][2])
        # print(vals.get('email'))
        vals['passwords'] = cryptocode.encrypt(vals.get('passwords'), get_key())
        temp_rec = self.env.ref('credential_manager.info_email_template')
        temp_rec.write({'email_to': vals.get('email')})
        temp_rec.write({'body_html': "Thank you for signing in!\n Username: " + vals.get(
            'email') + "\n Password: " + vals.get('passwords')})
        temp_rec.send_mail(self.id, force_send=True)

        followers_ids = vals.get('partner_ids')[0][2]
        # add followers to group follower
        follower_group = self.env.ref('credential_manager.group_followers')
        for follower in followers_ids:
            follower_group.write({'users': [(4, follower)]})
        return super(CredentialManager, self).create(vals)

    def action_notify_email(self):
        followers_ids = []
        for i in self.partner_ids:
            followers_ids.append(i.partner_id.id)
        print('followers', followers_ids)
        for follower in followers_ids:
            temp_rec = self.env.ref('credential_manager.notify_email_template')
            temp_rec.write({'partner_to': follower})
            temp_rec.send_mail(self.id, force_send=True)
