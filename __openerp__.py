# -*- coding: utf-8 -*-

{
    'name': 'Fiche Article',
    'version': '1.0',
    'category': 'InfoSaône',
    'description': """
Ameliorer la fiche article
""",
    'author': 'Tony GALMICHE / Asma BOUSSELMI',
    'maintainer': 'InfoSaone',
    'website': 'http://www.infosaone.com',
    'depends': [
        'product', 
        'sale',
        'is_mrp',
    ],
    'data': ['security/is_pg_security.xml',
             'security/ir.model.access.csv',
             'view/is_product_view.xml',
             'is_category.xml',
             'is_gestionnaire.xml',
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
