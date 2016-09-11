# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import time
import re
from openerp import pooler
from openerp.osv import osv, fields, expression
from openerp.tools.translate import _



class is_section_analytique(osv.osv):
    _name = 'is.section.analytique'
    _description = 'Section analytique'
    
    _columns = {
        'name': fields.char('Section analytique', required=True),
    }

class is_budget_responsable(osv.osv):
    _name = 'is.budget.responsable'
    _columns = {
        'name': fields.char('Responsable budget', required=True),
    }

class is_budget_nature(osv.osv):
    _name = 'is.budget.nature'
    _columns = {
        'name': fields.char('Nature budget', required=True),
    }


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

# Cette class permet : 
# - d'ajouter le moule à la class d'origine. 
# - de changer l'ordre de tri par défaut
# - d'ajouter une contrainte unique sur le code de l'article
# - de gérer la duplication de l'article

class product_product(osv.osv):
    _inherit = 'product.product'

    def name_get(self, cr, uid, ids, context=None):
        #if not len(ids):
        #    return []
        res = []
        for product in self.browse(cr, uid, ids, context=context):
            name=product.is_code+" "+product.name
            res.append((product.id,name))
        return res



    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            ids = []
            if operator in positive_operators:
                ids = self.search(cr, user, [('is_code','=',name)]+ args, limit=limit, context=context)
                if not ids:
                    ids = self.search(cr, user, [('ean13','=',name)]+ args, limit=limit, context=context)
            if not ids and operator not in expression.NEGATIVE_TERM_OPERATORS:
                ids = self.search(cr, user, args + [('is_code', operator, name)], limit=limit, context=context)
                if not limit or len(ids) < limit:
                    limit2 = (limit - len(ids)) if limit else False
                    ids += self.search(cr, user, args + [('name', operator, name), ('id', 'not in', ids)], limit=limit2, context=context)
            elif not ids and operator in expression.NEGATIVE_TERM_OPERATORS:
                ids = self.search(cr, user, args + ['&', ('is_code', operator, name), ('name', operator, name)], limit=limit, context=context)
            if not ids and operator in positive_operators:
                ptrn = re.compile('(\[(.*?)\])')
                res = ptrn.search(name)
                if res:
                    ids = self.search(cr, user, [('is_code','=', res.group(2))] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        result = self.name_get(cr, user, ids, context=context)
        return result











class product_template(osv.osv):
    _inherit = 'product.template'
    _order='is_code'
    _sql_constraints = [('is_default_code_uniq','UNIQUE(is_code)', 'Ce code existe déjà')]    

    _columns = {
        'is_code' : fields.char('Code PG', select=True, required=True),

        'segment_id': fields.many2one('is.product.segment', 'Segment', required=True),
        'family_id': fields.many2one('is.product.famille', 'Famille'),
        'sub_family_id': fields.many2one('is.product.sous.famille', 'Sous famille'),

        'is_category_id': fields.many2one('is.category', 'Catégorie'),
        'related_is_category_id': fields.boolean('Champ technique'),
        
        'is_gestionnaire_id': fields.many2one('is.gestionnaire', 'Gestionnaire'),
        'related_is_gestionnaire_id': fields.boolean('Champ technique'),
        
        'is_mold_id': fields.many2one('is.mold', 'Moule'),
        'related_is_mold_id': fields.boolean('Champ technique'),

        'is_dossierf_id': fields.many2one('is.dossierf', 'Dossier F'),
        'related_is_dossierf_id': fields.boolean('Champ technique'),

        'is_ref_client': fields.char('Référence client'),
        'related_is_ref_client': fields.boolean('Champ technique'),

        'is_client_id': fields.many2one('res.partner', 'Client par défaut', help="Ce champ est utilisé pour la liste des stocks par client et pour les étiquettes Galia"),
        'related_is_client_id': fields.boolean('Champ technique'),

        'is_ref_plan':   fields.char('Référence plan'),
        'related_is_ref_plan': fields.boolean('Champ technique'),
        
        'is_ind_plan':   fields.char('Indice plan'),
        'related_is_ind_plan': fields.boolean('Champ technique'),

        'is_nomenclature_douaniere': fields.char('Nomenclature douanière'),
        'related_is_nomenclature_douaniere': fields.boolean('Champ technique'),

        'is_stock_secu': fields.integer('Stock de sécurité'),
        'related_is_stock_secu': fields.boolean('Champ technique'),


        'is_soumise_regl': fields.selection([('SR','SR'),('R','R')], "Pièce soumise à réglementation"),
        'related_is_soumise_regl': fields.boolean('Champ technique'),
        
        'is_livree_aqp':  fields.boolean('Pièce livrée en AQP'),
        'related_is_livree_aqp': fields.boolean('Champ technique'),
        
        'is_droite_grauche': fields.selection([('D','D'),('G','G')], "Pièce droite/gauche"),
        'related_is_droite_grauche': fields.boolean('Champ technique'),

        'is_couleur': fields.char('Couleur / Type matière', help="Mettre la couleur pour les matières et la matière pour les produits fabriqués"),
        'related_is_couleur': fields.boolean('Champ technique'),

        'is_perte': fields.float('% de perte'),
        'related_is_perte': fields.boolean('Champ technique'),
        
        'is_destockage':  fields.boolean('Déstockage automatique nomenclature'),
        'related_is_destockage': fields.boolean('Champ technique'),

        'is_ref_fournisseur': fields.char('Référence fournisseur'),
        'related_is_ref_fournisseur': fields.boolean('Champ technique'),
        
        'lot_mini': fields.float("Lot d'appro."),
        'related_lot_mini': fields.boolean('Champ technique'),
        
        'multiple': fields.float('Multiple de'),
        'related_multiple': fields.boolean('Champ technique'),
        
        'delai_cq': fields.float('Délai contrôle qualité'),
        'related_delai_cq': fields.boolean('Champ technique'),
        
        'temps_realisation': fields.float('Temps de realisation en secondes'),
        'related_temps_realisation': fields.boolean('Champ technique'),

        'is_origine_produit_id': fields.many2one('res.country', 'Origine du produit'),
        'related_is_origine_produit_id': fields.boolean('Champ technique'),

        'is_produit_perissable': fields.boolean('Produit périssable'),
        'related_is_produit_perissable': fields.boolean('Champ technique'),

        # related fields
        'related_default_code':  fields.boolean('Champ technique'),
        'related_ean13': fields.boolean('Champ technique'),
        'related_lst_price': fields.boolean('Champ technique'),
        
        'lot_livraison': fields.float('Lot de livraison'),
        'multiple_livraison': fields.float('Multiple de livraison'),

        'is_section_analytique_id': fields.many2one('is.section.analytique', 'Section analytique'),

        'is_budget_responsable_id': fields.many2one('is.budget.responsable', 'Responsable budget'),
        'is_budget_nature_id'     : fields.many2one('is.budget.nature'     , 'Nature budget'),
        'is_budget_fv': fields.selection([('F','Fixe'),('V','Variable')], "Budget Fixe ou Variable"),
    }
    
    _defaults = {        
        'related_is_category_id':  False,        
        'related_is_gestionnaire_id':  False,
        'related_is_mold_id':  False,
        'related_is_ref_client':  False,
        'related_is_ref_plan':  False,
        'related_is_ind_plan':  False,
        'related_is_stock_secu':  False,
        'related_is_soumise_regl':  False,       
        'related_is_livree_aqp':  False,
        'related_is_droite_grauche':  False,
        'related_is_couleur':  False,
        'related_is_perte':  False,       
        'related_is_destockage':  False,
        'related_is_ref_fournisseur':  False,
        'related_lot_mini':  False,
        'related_multiple':  False,
        'related_delai_fabrication':  False,
        'related_temps_realisation':  False,
        
        'related_ean13': False,
        'related_lst_price': False,
        
        'lot_mini': 0.0,
        'multiple': 1.0,
        'delai_fabrication': 0.0,
        'temps_realisation': 0.0,
    }


    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        res = []
        for product in self.browse(cr, uid, ids, context=context):
            #p_name = pckg.ean and '[' + pckg.ean + '] ' or ''
            #p_name += pckg.ul.name
            #name="["+product.is_code+"] "+product.name
            name=product.is_code+" "+product.name
            res.append((product.id,name))
        return res



    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            ids = []
            if operator in positive_operators:
                ids = self.search(cr, user, [('is_code','=',name)]+ args, limit=limit, context=context)
                if not ids:
                    ids = self.search(cr, user, [('ean13','=',name)]+ args, limit=limit, context=context)
            if not ids and operator not in expression.NEGATIVE_TERM_OPERATORS:
                ids = self.search(cr, user, args + [('is_code', operator, name)], limit=limit, context=context)
                if not limit or len(ids) < limit:
                    limit2 = (limit - len(ids)) if limit else False
                    ids += self.search(cr, user, args + [('name', operator, name), ('id', 'not in', ids)], limit=limit2, context=context)
            elif not ids and operator in expression.NEGATIVE_TERM_OPERATORS:
                ids = self.search(cr, user, args + ['&', ('is_code', operator, name), ('name', operator, name)], limit=limit, context=context)
            if not ids and operator in positive_operators:
                ptrn = re.compile('(\[(.*?)\])')
                res = ptrn.search(name)
                if res:
                    ids = self.search(cr, user, [('is_code','=', res.group(2))] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        result = self.name_get(cr, user, ids, context=context)
        return result



    

    def copy(self, cr, uid, id, default=None, context=None):
        if not context:
            context = {}
        product = self.read(cr, uid, id, ['is_code'], context=context)
        default.update({
            'is_code': product['is_code'] + _(' (copy)'),
        })
        return super(product_template, self).copy(cr, uid, id, default=default, context=context)

    # onchange_segment_id
    def onchange_segment_id(self, cr, uid, ids, segment_id, context=None):
        domain = []
        val = {'family_id': False,
                'sub_family_id': False,
        }            
        domain.append(('segment_id','=',segment_id))
        # gestion d'invisibilité des champs en fonction de la valeur de segment
        #Initialiser les champs related à False
        val.update({'related_is_category_id':  False,        
                    'related_is_gestionnaire_id':  False,
                    'related_is_mold_id':  False,
                    'related_is_ref_client':  False,
                    'related_is_ref_plan':  False,
                    'related_is_ind_plan':  False,
                    'related_is_stock_secu':  False,
                    'related_is_soumise_regl':  False,       
                    'related_is_livree_aqp':  False,
                    'related_is_droite_grauche':  False,
                    'related_is_couleur':  False,
                    'related_is_perte':  False,       
                    'related_is_destockage':  False,
                    'related_is_ref_fournisseur':  False,
                    'related_lot_mini':  False,
                    'related_multiple':  False,
                    'related_delai_fabrication':  False,
                    'related_temps_realisation':  False,                   
                    'related_ean13': False,
                    'related_lst_price': False,
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
    
#is_product_product() 

class is_product_view(osv.osv):
    _name = 'is.product.view'
    _description = 'Afficher et masquer des champs en fonction de segment'
    
    _columns = {
        'fields_id': fields.many2one('ir.model.fields', 'Champ', domain=[('model', '=', 'product.template'), 
                                                                         ('name','in',('is_category_id',     
                                                                                        'is_gestionnaire_id',
                                                                                        'is_mold_id',
                                                                                        'is_ref_client',
                                                                                        'is_ref_plan',
                                                                                        'is_ind_plan',
                                                                                        'is_stock_secu',
                                                                                        'is_soumise_regl',       
                                                                                        'is_livree_aqp',
                                                                                        'is_droite_grauche',
                                                                                        'is_couleur',
                                                                                        'is_perte',       
                                                                                        'is_destockage',
                                                                                        'is_ref_fournisseur',
                                                                                        'is_origine_produit_id',
                                                                                        'lot_mini',
                                                                                        'multiple',
                                                                                        'delai_fabrication',
                                                                                        'temps_realisation',                   
                                                                                        'ean13',
                                                                                        'lst_price',))], ondelete='cascade', required=True, select=1),
        'segment_id': fields.many2one('is.product.segment', 'Segement', required=True),
    }
    
is_product_view()





