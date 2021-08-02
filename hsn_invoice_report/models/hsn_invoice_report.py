# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models , fields


class AccountMove(models.Model):
    _inherit = "account.move"
    # Split the product based on HSN code
    def _getvat(self):
       mycompany= self.env['res.company'].search([('id','=',1)])
       self.vat=mycompany.vat
       print(mycompany.vat)

    vat = fields.Char(string ='vat', compute="_getvat")

    def print_report(self):

        return self.env.ref('hsn_invoice_report.action_report_customer_invoice').report_action(self)


    def get_hsn_code(self, hsn):
        list1 = []
        for invoice_line in self.invoice_line_ids:
            list1.append(invoice_line.product_id.l10n_in_hsn_code)
        hsn_group = list(set(list1))
        return hsn_group

    # Get Rate and Amount fot GST product
    def get_gst(self, inv_id, product_id):
        invoice = self.search([('id', '=', inv_id)], limit=1)
        tax_amount = 0
        rate = 0
        for num in invoice.invoice_line_ids:
            if num.product_id.id == product_id:
                tax_rate = 0
                for i in num.tax_ids:
                    if i.children_tax_ids:
                        tax_rate = sum(i.children_tax_ids.mapped('amount'))
                tax_amount = ((tax_rate / 100) * num.price_subtotal) / 2
                rate = tax_rate / 2
        return [rate, tax_amount]

    # Get Rate and Amount fot IGST product
    def get_igst(self, inv_id, product_id):
        invoice = self.search([('id', '=', inv_id)], limit=1)
        tax_amount = 0
        rate = 0
        for i in invoice.invoice_line_ids:
            if i.product_id.id == product_id:
                tax_rate = 0
                for t in i.tax_ids:
                    if not t.children_tax_ids:
                        tax_rate = t.amount
                tax_amount = (tax_rate / 100) * i.price_subtotal
                rate = tax_rate
        return [rate, tax_amount]
