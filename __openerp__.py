# -*- coding: utf-8 -*-

{
    'name': 'Fiche Article',
    'version': '1.0',
    'category': 'InfoSaone',
    'description': """
Ameliorer la fiche article
""",
    'author': 'Tony GALMICHE / Asma BOUSSELMI',
    'maintainer': 'InfoSaone',
    'website': 'http://www.infosaone.com',
    'depends': ['product', 'sale'],
    'data': ['security/is_pg_security.xml',
             'security/ir.model.access.csv',
             'view/is_product_view.xml',
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: