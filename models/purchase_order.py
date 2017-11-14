from openerp import api, fields, models
import openerp.addons.decimal_precision as dp


class PurchaseDiscountPurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    #@api.depends('discount')
    #def _compute_amount(self):
    #    prices = {}
    #    for line in self:
    #        if line.discount:
    #            prices[line.id] = line.price_unit
    #            line.price_unit *= (1 - line.discount / 100.0)
    #            line.net_price = line.price_unit

    #    super(PurchaseDiscountPurchaseOrderLine, self)._compute_amount()
    #    for line in self:
    #        if line.discount:
    #            line.price_unit = prices[line.id]

    @api.depends('product_qty', 'price_unit', 'taxes_id','discount')
    def _compute_amount(self):
        for line in self:
            prices = {}
            if line.discount:
                prices[line.id] = line.price_unit
                calculo = line.price_unit*(1 - line.discount / 100.0)
                line.net_price = calculo
                taxes = line.taxes_id.compute_all(line.net_price, line.order_id.currency_id, line.product_qty,
                                                  product=line.product_id, partner=line.order_id.partner_id)
                line.update({
                    'price_tax': taxes['total_included'] - taxes['total_excluded'],
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                })
                line.price_subtotal = taxes['total_excluded']

            else:
                line_prr = line.price_unit
                taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_qty,
                                                  product=line.product_id, partner=line.order_id.partner_id)
                line.update({
                    'price_tax': taxes['total_included'] - taxes['total_excluded'],
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                })
                line.price_subtotal = taxes['total_excluded']


    net_price = fields.Float(string='Precio neto', digits_compute=dp.get_precision('Product Price'), compute='_compute_amount')
    discount = fields.Float(string='Descuento (%)', digits_compute=dp.get_precision('Discount'))

    _sql_constraints = [
        ('discount_limit', 'CHECK (discount <= 100.0)',
         'Discount must be lower than 100%.'),
    ]
