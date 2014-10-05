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




#class product_product(osv.osv):
#    _inherit = 'product.product'
#    #_order='is_code'    

#    def name_get(self, cr, user, ids, context=None):
#        if context is None:
#            context = {}
#        code = context.get('display_default_code', True) and d.get('default_code',False) or False
#        return "test tony"




# Cette class permet : 
# - d'ajouter le moule à la class d'origine. 
# - de changer l'ordre de tri par défaut
# - d'ajouter une contrainte unique sur le code de l'article
# - de gérer la duplication de l'article

class is_product_product(osv.osv):
    _inherit = 'product.product'
    _order='default_code'
    _sql_constraints = [('is_default_code_uniq','UNIQUE(default_code)', 'Ce code existe déjà')]    

    _columns = {

        'default_code' : fields.char('Code', select=True, required=True),
        #'name': fields.char('Désignation', required=True, translate=True),

        'segment_id': fields.many2one('is.product.segment', 'Segment', required=True),
        'family_id': fields.many2one('is.product.famille', 'Famille'),
        'sub_family_id': fields.many2one('is.product.sous.famille', 'Sous famille'),

        'is_category_id': fields.many2one('is.category', 'Catégorie'),
        'is_gestionnaire_id': fields.many2one('is.gestionnaire', 'Gestionnaire'),
        'is_mold_id': fields.many2one('is.mold', 'N°Moule'),

        'is_ref_client': fields.char('Référence client'),
        'is_ref_plan':   fields.char('Référence plan'),
        'is_ind_plan':   fields.char('Indice plan'),

        'is_stock_secu': fields.integer('Stock de sécurité'),


        'is_soumise_regl': fields.selection([('SR','SR'),('R','R')], "Pièce soumise à réglementation"),
        'is_livree_aqp':  fields.boolean('Pièce livrée en AQP'),
        'is_droite_grauche': fields.selection([('D','D'),('G','G')], "Pièce droite/gauche"),

        'is_couleur': fields.char('Couleur'),

        'is_perte': fields.integer('% de perte'),
        'is_destockage':  fields.boolean('Déstockage automatique nomenclature'),

        'is_ref_fournisseur': fields.char('Référence fournisseur'),


        # related fields
        'related_default_code':  fields.boolean('Champ technique'),
        'related_ean13': fields.boolean('Champ technique'),
        'related_lst_price': fields.boolean('Champ technique'),

        'related_is_mold_id': fields.boolean('Champ technique'),
    }
    
    _defaults = {
        'related_default_code':  False,
        'related_ean13': False,
        'related_lst_price': False,

        'related_is_mold_id':  False,
    }
    


#    def name_get(self, cr, user, ids, context=None):
#        if context is None:
#            context = {}
#        if isinstance(ids, (int, long)):
#            ids = [ids]
#        if not len(ids):
#            return []

#        def _name_get(d):
#            name = d.get('name','')
#            code = context.get('display_default_code', True) and d.get('default_code',False) or False
#            if code:
#                name = '[%s] %s' % (code,name)
#            name="test tony"
#            return (d['id'], name)

#    def name_get(self, cr, user, ids, context=None):
#        if context is None:
#            context = {}
#        return "test tony"
#        #if 'partner_id' in context:
#        #    pass
#        #return super(product_template, self).name_get(cr, user, ids, context)






    def copy(self, cr, uid, id, default=None, context=None):
        if not context:
            context = {}
        product = self.read(cr, uid, id, ['default_code'], context=context)
        default.update({
            'default_code': product['default_code'] + _(' (copy)'),
        })
        return super(is_product_product, self).copy(cr, uid, id, default=default, context=context)




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
                    'related_lst_price': False,
                    'related_is_mold_id': False,
        })
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
        'fields_id': fields.many2one('ir.model.fields', 'Champ', domain=[('model', '=', 'product.product')], ondelete='cascade', required=True, select=1),
        'segment_id': fields.many2one('is.product.segment', 'Segement', required=True),
    }
    
is_product_view()





