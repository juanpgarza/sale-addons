# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ['sale.order', 'tier.validation']

    review_done_by_users = fields.Char(string='Aprobado Por',compute="_compute_review_user_ids",store=True)

    @api.depends('review_ids')
    def _compute_review_user_ids(self):
        for rec in self:
            if rec.review_ids:
                rec.review_done_by_users = ', '.join(rec.review_ids.mapped("done_by.name"))
            else:
                rec.review_done_by_users = False    