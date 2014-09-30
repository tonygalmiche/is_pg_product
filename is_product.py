# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _

class is_product_segment(osv.osv):
    _name = 'is.product.segment'
    _description = 'Segments des produits'
    
    _columns = {
        'name': fields.char('Code', size=256, required=True),
        'description': fields.text('Commentaire'),
        'family_line': fields.one2many('is.product.famille', 'segment_id', 'Familles'),
    }

is_product_segment()   

class is_product_famille(osv.osv):
    _name = 'is.product.famille'
    _description = 'Familles des produits'
    
    _columns = {
        'name': fields.char('Code', size=256, required=True),
        'segment_id': fields.many2one('is.product.segment', 'Segment', required=True),
        'description': fields.text('Commentaire'),
        'sub_family_line': fields.one2many('is.product.sous.famille', 'family_id', 'Sous Familles'),
    }

is_product_famille()   

class is_product_sous_famille(osv.osv):
    _name = 'is.product.sous.famille'
    _description = 'Sous familles des produits'
    
    _columns = {
        'name': fields.char('Code', size=256, required=True),
        'family_id': fields.many2one('is.product.famille', 'Famille', required=True),
        'description': fields.text('Commentaire'),
    }

is_product_sous_famille() 

class is_product_product(osv.osv):
    _inherit = 'product.template'
    
    _columns = {
        'segment_id': fields.many2one('is.product.segment', 'Segment', required=True),
        'family_id': fields.many2one('is.product.famille', 'Famille'),
        'sub_family_id': fields.many2one('is.product.sous.famille', 'Sous famille'),
        # related fields
        'related_default_code':  fields.boolean('Champ technique'),
        'related_ean13': fields.boolean('Champ technique'),
        'related_lst_price': fields.boolean('Champ technique'),
    }
    
    _defaults = {
        'related_default_code':  False,
        'related_ean13': False,
        'related_lst_price': False,
    }
    
    # onchange_segment_id
    def onchange_segment_id(self, cr, uid, ids, segment_id, context=None):
        domain = []
        val = {'family_id': False,
                'sub_family_id': False,
        }            
        domain.append(('segment_id','=',segment_id))
        # gestion d'invisibilité des champs en fonction de la valeur de segment
        #Initialiser les champs related à False
        val.update({'related_default_code': False,
                    'related_ean13': False,
                    'related_lst_price': False,})
        if segment_id:
            invisible_obj = self.pool.get('is.product.view')
            invisible_ids = invisible_obj.search(cr, uid, [('segment_id', '=', segment_id)], context=context)
            if invisible_ids:
                for item in invisible_obj.browse(cr, uid, invisible_ids, context=context):
                    field = str('related_'+item.fields_id.name)
                    val.update({field: True})

        return {'value': val,
                'domain': {'family_id': domain}}
        
    # onchange_family_id
    def onchange_family_id(self, cr, uid, ids, family_id, context=None):
        domain = []
        val = {'sub_family_id': False}
            
        domain.append(('family_id','=',family_id))
        return {'value': val,
                'domain': {'sub_family_id': domain}}
    
is_product_product() 

class is_product_view(osv.osv):
    _name = 'is.product.view'
    _description = 'Afficher et masquer des champs en fonction de segment'
    
    _columns = {
        'fields_id': fields.many2one('ir.model.fields', 'Champ', domain=[('model', '=', 'product.template')], ondelete='cascade', required=True, select=1),
        'segment_id': fields.many2one('is.product.segment', 'Segement', required=True),
    }
    
is_product_view()