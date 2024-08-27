from odoo import models, fields, api

class ProductPricelistTemp(models.Model):
    _name = 'product.pricelist.temp'
    _description = 'Tarifas Temporales'

    default_code = fields.Char(string="Referencia interna", related='product_id.default_code') 
    product_id = fields.Many2one('product.product', 'Producto')
    name = fields.Text(string="Descripción de ventas", related='product_id.description_sale')     
    # price = fields.Monetary("Precio")
    pricelist_id = fields.Many2one('product.pricelist', 'Tarifa')
    currency_id = fields.Many2one(
        'res.currency', 'Moneda',
        readonly=True, related='pricelist_id.currency_id', store=True)
    price = fields.Float("Precio", digits='Product Price')
    active = fields.Boolean(default=True)

    @api.model
    def _actualizar_tarifas(self, pricelist_id = 8):
        products = self.env['product.product'].search([])
        # pricelist_id_comercio_pesos = 8
        self.env['product.pricelist.temp'].search([]).unlink()
        for rec in products.filtered(lambda x: x.sale_ok and x.detailed_type == 'product'):
            price = self.env['product.product'].browse(rec.id).with_context(pricelist=pricelist_id).price
            vals = {
                    'product_id': rec.id,
                    'price': price,
                    'pricelist_id': pricelist_id}
            
            self.env['product.pricelist.temp'].create(vals)
