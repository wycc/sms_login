# -*- coding: utf-8 -*-
{
    'name': "sms_login",

    'summary': """
        Signup and reset the password by using the SMS message.
        """,

    'description': """
        Use SMS instead of the E-mail to signup and reset the password.
    """,

    'author': "Yu-Chung Wang",
    'website': "http://www.homescenario.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base,auth_signup'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
