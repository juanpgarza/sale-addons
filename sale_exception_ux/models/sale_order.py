# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    # _inherit = ['sale.order', 'base.exception']
    # _name = 'sale.order'
    _inherit = 'sale.order'

    @api.multi
    def check_sale_type(self):
        self.ensure_one()
        if self.type_id.id != self.partner_id.sale_type.id:
            return False
        return True

    @api.multi
    def check_discount_simple_product(self):
        self.ensure_one()
        # ["&","&","&",["order_line.discount",">",4],
        # ["order_line.pack_child_line_ids","=",False],["order_line.pack_parent_line_id","=",False],"|",["state","=","draft"],["state","=","sent"]]
        for line in self.order_line:
            if line.discount > 4 and not line.pack_child_line_ids and not line.pack_parent_line_id:
                return False           
        return True

    @api.multi
    def check_discount_pack_product(self):
        self.ensure_one()
        for line in self.order_line:
            if line.discount > 10 and line.pack_child_line_ids and line.pack_parent_line_id:
                return False
        return True

    # @api.multi
    # def check_discount_pack_component_product(self):
    #     self.ensure_one()
    #     for line in self.order_line:
    #         if line.discount > 10 and line.pack_child_line_ids and line.pack_parent_line_id:
    #             return False
    #     return True

class SaleOrder(models.Model):
    _inherit = ['sale.order', 'base.exception']
    _name = 'sale.order'
    # _inherit = 'sale.order'

    unlocked = fields.Boolean("Pedido desbloqueado",default=False,copy=False)

    @api.multi
    def detect_exceptions(self):
        # if self.state == 'draft':
        if self.unlocked:
            res = super(SaleOrder, self).detect_exceptions()
            # import pdb; pdb.set_trace()
        else:
            # con esto anulo el comportamiento por defecto del módulo
            # que es que pida autorización al confirmar un presupuesto
            res = False

        return res

    def _fields_trigger_check_exception(self):
        res = super(SaleOrder, self)._fields_trigger_check_exception()
        # addons-OCA/sale-workflow/sale_exception/models/sale.py:52
        # res = ['ignore_exception', 'order_line', 'state']
        # esto es para que chequee las reglas cuando SOLO se cambia el tipo de venta (No se cambia el estado ni una linea)
        return res + ['type_id']

    def sale_check_exception(self):        
        orders = self.filtered(lambda s: s.state == 'sale')
        for rec in orders:
            # import pdb; pdb.set_trace()
            # orders._check_exception()
            if rec.detect_exceptions():
                # import pdb; pdb.set_trace()
                return rec._popup_exceptions()

    @api.multi
    def action_done(self):
        for rec in self:
            if rec.detect_exceptions() and not rec.ignore_exception and rec.unlocked:
                raise ValidationError('Debe resolver la excepción antes de poder bloquear el pedido')
        return super().action_done()

    @api.multi
    def action_unlock(self):
        for rec in self:
            rec.unlocked = True
            rec.ignore_exception = False
        return super().action_unlock()


    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        for rec in self:
            if rec.detect_exceptions() and not rec.ignore_exception and rec.unlocked:
                raise ValidationError('Debe resolver la excepción antes de poder facturar')

        res = super(SaleOrder, self).action_invoice_create(grouped, final)