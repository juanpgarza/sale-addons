from odoo import api, fields, models
from odoo.tools.translate import html_translate

# src/addons/sale_quotation_builder/models/sale_order.py
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    website_description_2 = fields.Html('Website Description 2', sanitize_attributes=False, translate=html_translate)

    # @api.onchange('partner_id')
    # def onchange_update_description_lang(self):
    #     super(SaleOrder,self).onchange_update_description_lang()
    #     if not self.sale_order_template_id:
    #         return
    #     else:
    #         template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)
    #         import pdb; pdb.set_trace()
    #         self.website_description_2 = template.website_description_2

    # def _compute_line_data_for_template_change(self, line):
    #     vals = super(SaleOrder, self)._compute_line_data_for_template_change(line)
    #     vals.update(website_description_2=line.website_description_2)
    #     return vals

    # def _compute_option_data_for_template_change(self, option):
    #     vals = super(SaleOrder, self)._compute_option_data_for_template_change(option)
    #     vals.update(website_description_2=option.website_description_2)
    #     return vals

    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        ret = super(SaleOrder, self).onchange_sale_order_template_id()
        if self.sale_order_template_id:
            template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)
            # import pdb; pdb.set_trace()
            self.website_description_2 = template.website_description_2
        return ret