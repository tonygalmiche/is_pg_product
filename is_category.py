# -*- coding: utf-8 -*-

from openerp import models,fields,api
from openerp.tools.translate import _

class is_category(models.Model):
    _name='is.category'
    _order='name'    #Ordre de tri par defaut des listes
    _sql_constraints = [('name_uniq','UNIQUE(name)', 'Ce code existe déjà')] 

    name         = fields.Char("Code",size=40,required=True, select=True)
    commentaire  = fields.Char('Intitulé')
    fantome      = fields.Boolean('Article fantôme', \
        help="Si cette case est cochée, les articles de cette catégorie passeront en fantôme dans les composants de la nomenclature")



