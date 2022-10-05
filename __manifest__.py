# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Credential Manager',
    'version': '1.0',
    'summary': 'Credential Manager Software',
    'sequence': 10,
    'description': """Credential Manager Software""",
    'category': 'Productivity',
    'license': 'LGPL-3',
    'website': 'https://www.osit.com.sa',
    'depends': ['mail'],
    'data': ['security/res_groups.xml',
             'security/security.xml',
             'security/ir.model.access.csv',
             'data/mail_template.xml',
             'views/credential_view.xml',
             ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
