# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class payment_register(models.TransientModel):
    _inherit = 'account.payment.register'

    payment_option = fields.Selection(
        [('full', 'Full Payment without Deduction'), ('partial', 'Full Payment with Deduction')], default='full',
        required=True, string='Payment Option')
    amount_pay_total = fields.Float('Amount Total', readonly=1)
    writeoff_multi_acc_ids = fields.One2many('writeoff.multi', 'register_id', string='Write Off Accounts')

    @api.model
    def default_get(self, fields):
        rec = super(payment_register, self).default_get(fields)
        rec.update({
            'amount_pay_total': rec.get('amount', 0),
        })
        return rec

    @api.onchange('writeoff_multi_acc_ids')
    def onchange_writeoff_multi_accounts(self):
        if self.writeoff_multi_acc_ids:
            diff_amount = sum([line.amount_payment for line in self.writeoff_multi_acc_ids])
            self.amount = self.amount_pay_total - diff_amount

    def _prepare_payment_vals(self, invoices):
        res = super(payment_register, self)._prepare_payment_vals(invoices)
        if self.writeoff_multi_acc_ids:
            multi_accounts = []
            diff_amount = 0.0
            for line in self.writeoff_multi_acc_ids:
                multi_accounts.append((0, 0, {'writeoff_account_id': line.writeoff_account_id.id,
                                              'name': line.name or '',
                                              'amt_percent': line.amt_percent or '',
                                              'amount': line.amount_payment or '',
                                              'currency_id': line.currency_id and line.currency_id.id or ''}))
                diff_amount += line.amount_payment
            res.update({
                'payment_option': 'partial',
                'payment_difference_handling': 'reconcile',
                'post_diff_acc': 'multi',
                'payment_difference': diff_amount,
                'writeoff_multi_acc_ids': multi_accounts
            })
        return res


class account_payment(models.Model):
    _inherit = "account.payment"

    payment_option = fields.Selection(
        [('full', 'Full Payment without Deduction'), ('partial', 'Full Payment with Deduction')], default='full',
        required=True, string='Payment Option')
    post_diff_acc = fields.Selection([('single', 'Single Account'), ('multi', 'Multiple Accounts')], default='single',
                                     string='Post Difference In To')
    writeoff_multi_acc_ids = fields.One2many('writeoff.accounts', 'payment_id', string='Write Off Accounts')

    @api.onchange('payment_option')
    def onchange_payment_option(self):
        if self.payment_option == 'full':
            self.payment_difference_handling = 'open'
            self.post_diff_acc = 'single'
        else:
            self.payment_difference_handling = 'reconcile'
            self.post_diff_acc = 'multi'

    @api.onchange('writeoff_multi_acc_ids')
    def onchange_writeoff_multi_accounts(self):
        if self.writeoff_multi_acc_ids:
            diff_amount = sum([line.amount for line in self.writeoff_multi_acc_ids])
            self.amount = self.invoice_ids and self.invoice_ids[0].amount_residual - diff_amount

    def post(self):
        for move in self:
            if move.payment_difference_handling == 'reconcile' and move.post_diff_acc == 'multi':
                amount = 0
                for payment in move.writeoff_multi_acc_ids:
                    amount += payment.amount
                if move.payment_type == 'inbound' and round(move.payment_difference, 2) != round(amount, 2):
                    raise UserError(_("The sum of write off amounts and payment difference amounts are not equal."))
                elif move.payment_type == 'outbound' and round(move.payment_difference, 2) != -round(amount, 2):
                    raise UserError(_("The sum of write off amounts and payment difference amounts are not equal."))
        return super(account_payment, self).post()

    def _prepare_payment_moves(self):
        if not self.post_diff_acc == 'multi':
            return super(account_payment, self)._prepare_payment_moves()
        all_move_vals = []
        for payment in self:
            company_currency = payment.company_id.currency_id
            move_names = payment.move_name.split(
                payment._get_move_name_transfer_separator()) if payment.move_name else None

            write_off_amount = payment.payment_difference_handling == 'reconcile' and -payment.payment_difference or 0.0
            if payment.payment_type in ('outbound', 'transfer'):
                counterpart_amount = payment.amount
                liquidity_line_account = payment.journal_id.default_debit_account_id
            else:
                counterpart_amount = -payment.amount
                liquidity_line_account = payment.journal_id.default_credit_account_id

            if payment.currency_id == company_currency:
                balance = counterpart_amount
                write_off_balance = write_off_amount
                counterpart_amount = write_off_amount = 0.0
                currency_id = False
            else:
                balance = payment.currency_id._convert(counterpart_amount, company_currency, payment.company_id,
                                                       payment.payment_date)
                write_off_balance = payment.currency_id._convert(write_off_amount, company_currency, payment.company_id,
                                                                 payment.payment_date)
                currency_id = payment.currency_id.id

            if payment.journal_id.currency_id and payment.currency_id != payment.journal_id.currency_id:
                liquidity_line_currency_id = payment.journal_id.currency_id.id
                liquidity_amount = company_currency._convert(
                    balance, payment.journal_id.currency_id, payment.company_id, payment.payment_date)
            else:
                liquidity_line_currency_id = currency_id
                liquidity_amount = counterpart_amount

            rec_pay_line_name = ''
            if payment.payment_type == 'transfer':
                rec_pay_line_name = payment.name
            else:
                if payment.partner_type == 'customer':
                    if payment.payment_type == 'inbound':
                        rec_pay_line_name += _("Customer Payment")
                    elif payment.payment_type == 'outbound':
                        rec_pay_line_name += _("Customer Credit Note")
                elif payment.partner_type == 'supplier':
                    if payment.payment_type == 'inbound':
                        rec_pay_line_name += _("Vendor Credit Note")
                    elif payment.payment_type == 'outbound':
                        rec_pay_line_name += _("Vendor Payment")
                if payment.invoice_ids:
                    rec_pay_line_name += ': %s' % ', '.join(payment.invoice_ids.mapped('name'))

            if payment.payment_type == 'transfer':
                liquidity_line_name = _('Transfer to %s') % payment.destination_journal_id.name
            else:
                liquidity_line_name = payment.name


            move_vals = {
                'date': payment.payment_date,
                'ref': payment.communication,
                'journal_id': payment.journal_id.id,
                'currency_id': payment.journal_id.currency_id.id or payment.company_id.currency_id.id,
                'partner_id': payment.partner_id.id,
                'line_ids': [
                    (0, 0, {
                        'name': rec_pay_line_name,
                        'amount_currency': counterpart_amount + write_off_amount,
                        'currency_id': currency_id,
                        'debit': balance + write_off_balance > 0.0 and balance + write_off_balance or 0.0,
                        'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
                        'date_maturity': payment.payment_date,
                        'partner_id': payment.partner_id.id,
                        'account_id': payment.destination_account_id.id,
                        'payment_id': payment.id,
                    }),
                    (0, 0, {
                        'name': liquidity_line_name,
                        'amount_currency': -liquidity_amount,
                        'currency_id': liquidity_line_currency_id,
                        'debit': balance < 0.0 and -balance or 0.0,
                        'credit': balance > 0.0 and balance or 0.0,
                        'date_maturity': payment.payment_date,
                        'partner_id': payment.partner_id.id,
                        'account_id': liquidity_line_account.id,
                        'payment_id': payment.id,
                    }),
                ],
            }
            if write_off_balance:
                for woff_payment in self.writeoff_multi_acc_ids:
                    write_off_amount = payment.payment_difference_handling == 'reconcile' and -woff_payment.amount or 0.0
                    if payment.currency_id == company_currency:
                        write_off_balance = write_off_amount
                    else:
                        write_off_balance = payment.currency_id._convert(write_off_amount, company_currency,
                                                                         payment.company_id,
                                                                         payment.payment_date)
                    move_vals['line_ids'].append((0, 0, {
                        'name': woff_payment.name,
                        'amount_currency': -write_off_amount,
                        'currency_id': currency_id,
                        'debit': write_off_balance < 0.0 and -write_off_balance or 0.0,
                        'credit': write_off_balance > 0.0 and write_off_balance or 0.0,
                        'date_maturity': payment.payment_date,
                        'partner_id': payment.partner_id.id,
                        'account_id': woff_payment.writeoff_account_id.id,
                        'payment_id': payment.id,
                    }))
            if move_names:
                move_vals['name'] = move_names[0]

            all_move_vals.append(move_vals)

            if payment.payment_type == 'transfer':

                if payment.destination_journal_id.currency_id:
                    transfer_amount = payment.currency_id._convert(counterpart_amount,
                                                                   payment.destination_journal_id.currency_id,
                                                                   payment.company_id, payment.payment_date)
                else:
                    transfer_amount = 0.0

                transfer_move_vals = {
                    'date': payment.payment_date,
                    'ref': payment.communication,
                    'partner_id': payment.partner_id.id,
                    'journal_id': payment.destination_journal_id.id,
                    'line_ids': [
                        (0, 0, {
                            'name': payment.name,
                            'amount_currency': -counterpart_amount,
                            'currency_id': currency_id,
                            'debit': balance < 0.0 and -balance or 0.0,
                            'credit': balance > 0.0 and balance or 0.0,
                            'date_maturity': payment.payment_date,
                            'partner_id': payment.partner_id.id,
                            'account_id': payment.company_id.transfer_account_id.id,
                            'payment_id': payment.id,
                        }),
                        (0, 0, {
                            'name': _('Transfer from %s') % payment.journal_id.name,
                            'amount_currency': transfer_amount,
                            'currency_id': payment.destination_journal_id.currency_id.id,
                            'debit': balance > 0.0 and balance or 0.0,
                            'credit': balance < 0.0 and -balance or 0.0,
                            'date_maturity': payment.payment_date,
                            'partner_id': payment.partner_id.id,
                            'account_id': payment.destination_journal_id.default_credit_account_id.id,
                            'payment_id': payment.id,
                        }),
                    ],
                }
                if move_names and len(move_names) == 2:
                    transfer_move_vals['name'] = move_names[1]
                all_move_vals.append(transfer_move_vals)
        return all_move_vals


class writeoff_accounts(models.Model):
    _name = 'writeoff.accounts'

    writeoff_account_id = fields.Many2one('account.account', string="Difference Account",
                                          domain=[('deprecated', '=', False)], copy=False, required="1")
    name = fields.Char('Description')
    amt_percent = fields.Float(string='Amount(%)', digits=(16, 2))
    amount = fields.Monetary(string='Payment Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    payment_id = fields.Many2one('account.payment', string='Payment Record')

    @api.onchange('amt_percent')
    def _onchange_amt_percent(self):
        if self.amt_percent and self.amt_percent > 0:
            if self.payment_id.invoice_ids:
                self.amount = self.payment_id.invoice_ids[0].amount_total * self.amt_percent / 100


class RegisterWriteoffMulti(models.TransientModel):
    _name = 'writeoff.multi'

    writeoff_account_id = fields.Many2one('account.account', string="Difference Account",
                                          domain=[('deprecated', '=', False)], copy=False, required="1")
    name = fields.Char('Description')
    amt_percent = fields.Float(string='Amount(%)', digits=(16, 2))
    amount_payment = fields.Monetary(string='Payment Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    register_id = fields.Many2one('account.payment.register', string='Register Record')

    @api.onchange('amt_percent')
    def _onchange_amt_percent(self):
        if self.amt_percent and self.amt_percent > 0:
            if self.register_id.amount_pay_total:
                self.amount_payment = self.register_id.amount_pay_total * self.amt_percent / 100
