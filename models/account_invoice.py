from openerp import api, models


class PurchaseDiscountAccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.model
    def new(self, values=None):
        values = {} if values is None else values
        account_invoice_line = super(
            PurchaseDiscountAccountInvoiceLine, self).new(values=values)
        if account_invoice_line.purchase_line_id:
            account_invoice_line.discount =\
                account_invoice_line.purchase_line_id.discount
        return account_invoice_line
