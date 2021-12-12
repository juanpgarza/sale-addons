##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, models, _
from odoo.tools import float_compare
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # src/addons-adhoc/sale/sale_order_type_invoice_policy/models/stock_picking.py:44
    def _check_sale_paid(self):
        # import pdb; pdb.set_trace()
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        invoice_status = self.sale_id.mapped(
            'order_line.invoice_lines.invoice_id.state')
        if (set(invoice_status) - set(['paid','cancel'])) or any(
                (float_compare(line.product_uom_qty,
                               line.qty_invoiced,
                               precision_digits=precision) > 0)
                for line in self.sale_id.order_line):
            return False
        return True
