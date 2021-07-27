from odoo import models, fields, api, _

class SaleCouponProgram(models.Model):
    _inherit = 'sale.coupon.program'

    @api.multi
    def write(self, values):
        res = super(SaleCouponProgram,self).write(values)   

        # import pdb; pdb.set_trace()

        nombre = 'Promo '
        if self.reward_type == 'discount':
            nombre = nombre + 'descuento'
        elif self.reward_type == 'product':
            nombre = nombre + 'producto gratis'
        else:
            nombre = nombre + 'envío gratis'

        product_values = {
            'name': nombre,
            'sale_ok': True,
            'description_sale': nombre,
            'registrar_novedad_presupuesto': False,
        }

        self.mapped('discount_line_product_id').write(product_values)

        return res
