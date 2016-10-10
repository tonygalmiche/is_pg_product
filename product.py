# -*- coding: utf-8 -*-

#from openerp.osv import osv, fields, expression

from openerp.osv import expression
from openerp import models,fields,api
from openerp.tools.translate import _



class is_config_champ(models.Model):
    _name='is.config.champ'
    _order='name'

    name        = fields.Many2one('is.product.segment', 'Segment à paramètrer', required=False)
    champs_line = fields.One2many('is.config.champ.line', 'segment_id', 'Champs')

    _sql_constraints = [
        ('name_uniq'       , 'unique(name)'       , u"Ce formulaire existe déja !"),
    ]


    @api.multi
    def copy(self,vals):
        for obj in self:
            vals.update({
                'name' : False,
            })
            res=super(is_config_champ, self).copy(vals)
            for item in obj.champs_line:
                v = {
                    'segment_id': res.id,
                    'name'      : item.name.id,
                    'vsb'       : item.vsb,
                }
                id = self.env['is.config.champ.line'].create(v)
            return res




class is_config_champ_line(models.Model):
    _name='is.config.champ.line'
    _order='segment_id,name'

    segment_id = fields.Many2one('is.config.champ', 'Segment à paramètrer')
    name     = fields.Many2one('ir.model.fields', 'Champ', domain=[
            ('model_id.model', '=','product.template' ),
            ('name', 'like', '_vsb'),
            ('field_description', '!=', 'Champ technique'),
        ]
    )

    vsb      = fields.Boolean('Visible')
    _defaults = {
        'vsb': False,
    }





class is_category(models.Model):
    _name='is.category'
    _order='name'    #Ordre de tri par defaut des listes
    _sql_constraints = [('name_uniq','UNIQUE(name)', 'Ce code existe déjà')] 
    name         = fields.Char("Code",size=40,required=True, select=True)
    commentaire  = fields.Char('Intitulé')
    fantome      = fields.Boolean('Article fantôme', \
        help="Si cette case est cochée, les articles de cette catégorie passeront en fantôme dans les composants de la nomenclature")


class is_gestionnaire(models.Model):
    _name='is.gestionnaire'
    _order='name'
    _sql_constraints = [('name_uniq','UNIQUE(name)', 'Ce code existe déjà')] 

    name        = fields.Char("Code",size=40,required=True, select=True)
    commentaire = fields.Text('Commentaire')


class is_section_analytique(models.Model):
    _name = 'is.section.analytique'
    _description = 'Section analytique'
    name = fields.Char('Section analytique', required=True)


class is_budget_responsable(models.Model):
    _name = 'is.budget.responsable'
    name = fields.Char('Responsable budget', required=True)


class is_budget_nature(models.Model):
    _name = 'is.budget.nature'
    name = fields.Char('Nature budget', required=True)


class is_product_segment(models.Model):
    _name = 'is.product.segment'
    _description = 'Segments des produits'
    name         = fields.Char('Code', size=256, required=True)
    description  = fields.Text('Commentaire')
    family_line  = fields.One2many('is.product.famille', 'segment_id', 'Familles')


class is_product_famille(models.Model):
    _name = 'is.product.famille'
    _description = 'Familles des produits'
    name            = fields.Char('Code', size=256, required=True)
    segment_id      = fields.Many2one('is.product.segment', 'Segment', required=True)
    description     = fields.Text('Commentaire')
    sub_family_line = fields.One2many('is.product.sous.famille', 'family_id', 'Sous Familles')


class is_product_sous_famille(models.Model):
    _name = 'is.product.sous.famille'
    _description = 'Sous familles des produits'
    name        = fields.Char('Code', size=256, required=True)
    family_id   = fields.Many2one('is.product.famille', 'Famille', required=True)
    description = fields.Text('Commentaire')




class product_template(models.Model):
    _inherit = 'product.template'
    _order='is_code'
    _sql_constraints = [('is_default_code_uniq','UNIQUE(is_code)', 'Ce code existe déjà')]

    @api.depends('segment_id')
    def _compute(self):
        for obj in self:
            if len(obj.segment_id)==0:
                # Si pas de segment => Masquer tous les champs
                for model in self.env['ir.model'].search([['model','=',self._name]]):
                    for champ in model.field_id:
                        if champ.name[-4:]=='_vsb':
                            setattr(obj, champ.name, True)
            else:
                # Si segment => Afficher tous les champs
                for model in self.env['ir.model'].search([['model','=',self._name]]):
                    for champ in model.field_id:
                        if champ.name[-4:]=='_vsb':
                            setattr(obj, champ.name, False)

                # Masquer les champs indiqués
                config_champ=self.env['is.config.champ'].search([['name', '=', obj.segment_id.id]])
                for o in config_champ:
                    for line in o.champs_line:
                        if line.vsb==False:
                            setattr(obj, line.name.name, True)


    is_code                       = fields.Char('Code PG', select=True, required=True)
    segment_id                    = fields.Many2one('is.product.segment', 'Segment', required=True)
    family_id                     = fields.Many2one('is.product.famille', 'Famille')
    sub_family_id                 = fields.Many2one('is.product.sous.famille', 'Sous famille')

    is_category_id                = fields.Many2one('is.category', 'Catégorie')
    is_category_id_vsb            = fields.Boolean('Catégorie', store=False, compute='_compute')

    is_gestionnaire_id            = fields.Many2one('is.gestionnaire', 'Gestionnaire')
    is_gestionnaire_id_vsb        = fields.Boolean('Gestionnaire', store=False, compute='_compute')

    is_mold_id                    = fields.Many2one('is.mold', 'Moule')
    is_mold_id_vsb                = fields.Boolean('Moule', store=False, compute='_compute')

    is_dossierf_id                = fields.Many2one('is.dossierf', 'Dossier F')
    is_dossierf_id_vsb            = fields.Boolean('Dossier F', store=False, compute='_compute')

    is_ref_client                 = fields.Char('Référence client')
    is_ref_client_vsb             = fields.Boolean('Référence client', store=False, compute='_compute')

    is_client_id                  = fields.Many2one('res.partner', 'Client par défaut', help="Ce champ est utilisé pour la liste des stocks par client et pour les étiquettes Galia")
    is_client_id_vsb              = fields.Boolean('Client par défaut', store=False, compute='_compute')

    is_ref_plan                   = fields.Char('Référence plan')
    is_ref_plan_vsb               = fields.Boolean('Référence plan', store=False, compute='_compute')

    is_ind_plan                   = fields.Char('Indice plan')
    is_ind_plan_vsb               = fields.Boolean('Indice plan', store=False, compute='_compute')

    is_nomenclature_douaniere     = fields.Char('Nomenclature douanière')
    is_nomenclature_douaniere_vsb = fields.Boolean('Nomenclature douanière', store=False, compute='_compute')

    is_stock_secu                 = fields.Integer('Stock de sécurité')
    is_stock_secu_vsb             = fields.Boolean('Stock de sécurité', store=False, compute='_compute')

    is_soumise_regl               = fields.Selection([('SR','SR'),('R','R')], "Pièce soumise à réglementation")
    is_soumise_regl_vsb           = fields.Boolean('Pièce soumise à réglementation', store=False, compute='_compute')

    is_livree_aqp                 = fields.Boolean('Pièce livrée en AQP')
    is_livree_aqp_vsb             = fields.Boolean('Pièce livrée en AQP', store=False, compute='_compute')

    is_droite_grauche             = fields.Selection([('D','D'),('G','G')], "Pièce droite/gauche")
    is_droite_grauche_vsb         = fields.Boolean('Pièce droite/gauche', store=False, compute='_compute')

    is_couleur                    = fields.Char('Couleur / Type matière', help="Mettre la couleur pour les matières et la matière pour les produits fabriqués")
    is_couleur_vsb                = fields.Boolean('Couleur / Type matière', store=False, compute='_compute')

    is_perte                      = fields.Float('% de perte')
    is_perte_vsb                  = fields.Boolean('% de perte', store=False, compute='_compute')

    is_destockage                 = fields.Boolean('Déstockage automatique nomenclature')
    is_destockage_vsb             = fields.Boolean('Déstockage automatique nomenclature', store=False, compute='_compute')

    is_ref_fournisseur            = fields.Char('Référence fournisseur')
    is_ref_fournisseur_vsb        = fields.Boolean('Référence fournisseur', store=False, compute='_compute')
    
    lot_mini                      = fields.Float("Lot d'appro.")
    lot_mini_vsb                  = fields.Boolean("Lot d'appro.", store=False, compute='_compute')

    multiple                      = fields.Float('Multiple de')
    multiple_vsb                  = fields.Boolean('Multiple de', store=False, compute='_compute')

    delai_cq                      = fields.Float('Délai contrôle qualité')
    delai_cq_vsb                  = fields.Boolean('Délai contrôle qualité', store=False, compute='_compute')

    temps_realisation             = fields.Float('Temps de realisation en secondes')
    temps_realisation_vsb         = fields.Boolean('Temps de realisation en secondes', store=False, compute='_compute')

    is_origine_produit_id         = fields.Many2one('res.country', 'Origine du produit')
    is_origine_produit_id_vsb     = fields.Boolean('Origine du produit', store=False, compute='_compute')

    is_produit_perissable         = fields.Boolean('Produit périssable')
    is_produit_perissable_vsb     = fields.Boolean('Produit périssable', store=False, compute='_compute')




    lot_livraison                 = fields.Float('Lot de livraison')
    lot_livraison_vsb             = fields.Boolean('Lot de livraison', store=False, compute='_compute')

    multiple_livraison            = fields.Float('Multiple de livraison')
    multiple_livraison_vsb        = fields.Boolean('Multiple de livraison', store=False, compute='_compute')

    is_section_analytique_id      = fields.Many2one('is.section.analytique', 'Section analytique')
    is_section_analytique_id_vsb  = fields.Boolean('Section analytique', store=False, compute='_compute')

    is_budget_responsable_id      = fields.Many2one('is.budget.responsable', 'Responsable budget')
    is_budget_responsable_id_vsb  = fields.Boolean('Responsable budget', store=False, compute='_compute')

    is_budget_nature_id           = fields.Many2one('is.budget.nature'     , 'Nature budget')
    is_budget_nature_id_vsb       = fields.Boolean('Nature budget', store=False, compute='_compute')

    is_budget_fv                  = fields.Selection([('F','Fixe'),('V','Variable')], "Budget Fixe ou Variable")
    is_budget_fv_vsb              = fields.Boolean('Budget Fixe ou Variable', store=False, compute='_compute')

    
    _defaults = {        
        'list_price': 0.0,
        'standard_price': 0.0,
        'lot_mini': 0.0,
        'multiple': 1.0,
        'delai_fabrication': 0.0,
        'temps_realisation': 0.0,
    }


    def name_get(self, cr, uid, ids, context=None):
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


    def onchange_segment_id(self, cr, uid, ids, segment_id, context=None):
        domain = []
        val = {
            'family_id': False,
            'sub_family_id': False,
        }            
        domain.append(('segment_id','=',segment_id))
        return {
            'value': val,
            'domain': {'family_id': domain}
        }
        

    def onchange_family_id(self, cr, uid, ids, family_id, context=None):
        domain = []
        val = {'sub_family_id': False}
            
        domain.append(('family_id','=',family_id))
        return {
            'value': val,
            'domain': {'sub_family_id': domain}
        }
    





class product_product(models.Model):
    _inherit = 'product.product'

    def name_get(self, cr, uid, ids, context=None):
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



