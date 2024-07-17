from odoo import fields, models, api


class Cogs (models.Model):
    _inherit = 'account.move'



    def post(self):
        # OVERRIDE
        # Don't change anything on moves used to cancel another ones.
        if self._context.get('move_reverse_cancel'):
            return super(Cogs, self).post()
        # Post entries.
        res = super(Cogs, self).post()
        # Create additional COGS lines for customer invoices.
        self.env['ifrs.move.line'].create(self._stock_account_prepare_ifrs_lines_vals())
        self.env['analytic.move.line'].create(self._stock_account_prepare_ifrs_lines_vals())
        return res

    def button_draft(self):
        res = super(Cogs, self).button_draft()

        # Unlink the COGS lines generated during the 'post' method.
        ifrs_lines = self.env['ifrs.move.line'].search([('move_id' ,'=',self.id),('is_cogs' ,'=',True)])
        if bool(ifrs_lines):
            ifrs_lines.unlink()
        analytic_lines = self.env['analytic.move.line'].search([('move_id' ,'=',self.id),('is_cogs' ,'=',True)])
        if bool(analytic_lines):
            analytic_lines.unlink()
        return res

    # def button_cancel(self):
    #     # OVERRIDE
    #     res = super(Cogs, self).button_cancel()
    #
    #     # Unlink the COGS lines generated during the 'post' method.
    #     ifrs_lines = self.env['ifrs.move.line'].search([('move_id', '=', self.id), ('is_cogs', '=', True)])
    #     if bool(ifrs_lines):
    #         ifrs_lines.unlink()
    #     return res

    def _stock_account_prepare_ifrs_lines_vals(self):
        lines_vals_list = []
        for move in self:
            if not move.is_sale_document(include_receipts=True):
                continue
            #On evite les lignes de notes dans factures
            normal_lines = move.invoice_line_ids
            for line in normal_lines:

                # Filter out lines being not eligible for COGS.
                if not line.account_id or not line.account_id.code.startswith(('7')):
                    continue

                # Retrieve accounts needed to generate the COGS.
                #NOT NEEDED but to filtered right account we have to pass by
                accounts = (
                    line.product_id.product_tmpl_id
                    .with_context(force_company=line.company_id.id)
                    .get_product_accounts(fiscal_pos=move.fiscal_position_id)
                )
                debit_interim_account = accounts['stock_output']
                credit_expense_account = accounts['expense']
                if not credit_expense_account:
                    if self.type == 'out_refund':
                        credit_expense_account = self.journal_id.default_credit_account_id
                    else: # out_invoice/out_receipt
                        credit_expense_account = self.journal_id.default_debit_account_id
                if not debit_interim_account or not credit_expense_account:
                    continue

                # Compute accounting fields.
                sign = -1 if move.type == 'out_refund' else 1
                price_unit = line.product_id.standard_price
                balance = sign * line.quantity * price_unit
                section_stock = self.env['ifrs.section'].search([('name', '=', 'Stock de marchandise'), ('company_id', '=', self.company_id.id)])
                section_vente = self.env['ifrs.section'].search([('name', '=', "Coût de marchandise vendu"), ('company_id', '=', self.company_id.id)])

                # Add interim account line.
                #SORTIE DE STOCK
                lines_vals_list.append({'date': line.date,
                        'move_id': line.id,
                        'partner_id': self.partner_id.id,
                        'section_id': section_stock.id,
                        'name':line.name[:64],
                        'account_department_id': self.account_department_id.id,
                        'account_id': line.account_id.id,
                        'product_id': line.product_id.id,
                        'amount': balance * (-1),
                        'company_id': line.company_id.id,
                        'is_cogs': True
                        }
                )

                # Add expense account line.(Variation de stock)
                #COUT DE M/SE VENDUE
                lines_vals_list.append({'date': line.date,
                        'move_id': line.id,
                        'partner_id': self.partner_id.id,
                        'section_id': section_vente.id,
                        'name':line.name[:64],
                        'account_department_id': self.account_department_id.id,
                        'account_id': line.account_id.id,
                        'product_id': line.product_id.id,
                        'amount': balance,
                        'company_id': line.company_id.id,
                        'is_cogs': True
                        })

        return lines_vals_list
    


