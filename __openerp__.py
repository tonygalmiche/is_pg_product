# -*- coding: utf-8 -*-
{
    'name': 'Fiche Article',
    'version': '1.0',
    'category' : 'InfoSaône\Plastigray',
    'description': """
Ameliorer la fiche article
""",
    'author': 'Tony GALMICHE / Asma BOUSSELMI',
    'maintainer': 'InfoSaone',
    'website': 'http://www.infosaone.com',
    'depends': [
        'product', 
        'sale',
        'stock',
        #'is_mold'
    ],
    'data': [
        'security/is_pg_security.xml',
        'security/ir.model.access.csv',
        'is_product_view.xml',
        'is_category_view.xml',
        'is_gestionnaire_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

