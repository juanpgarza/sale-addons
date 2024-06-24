# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HowKnowAboutUs(models.Model):
    _name = 'how.know.about.us'
    _description = 'Como nos conoció'

    name = fields.Char(string='Descripción')