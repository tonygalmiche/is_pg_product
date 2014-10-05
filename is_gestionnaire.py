# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp.tools.translate import _

class is_gestionnaire(osv.osv):
    _name='is.gestionnaire'
    _order='name'    #Ordre de tri par defaut des listes
    _sql_constraints = [('name_uniq','UNIQUE(name)', 'Ce code existe déjà')] 


    #ATTENTION : Pour que la relation many2one affiche le code du moule, le champ doit être nommé 'name' sinon il faut surcharger la méthode name_get
    _columns={
        'name':fields.char("Code",size=40,required=True, select=True),
        'commentaire': fields.text('Commentaire'),
    }

is_gestionnaire()

