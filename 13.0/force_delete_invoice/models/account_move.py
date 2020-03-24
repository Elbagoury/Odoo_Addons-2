from odoo import models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def force_unlink(self):
        Payment = self.env['account.payment'].sudo()
        move_type = ''
        for move in self:
            if move.state not in ['posted', 'cancel'] and not self._context.get('force_delete'):
                raise UserError(_("You cannot delete an invoice that has not been canceled."))
            payments = Payment.search([('invoice_ids', 'in', move.ids)])
            if payments:
                payments.action_draft()
                payments.move_name = ''
                payments.unlink()
            move_type = move.type
            move.with_context(force_delete=True).unlink()

        try:
           tree_id = self.env.ref('account.view_invoice_tree').id
           form_id = self.env.ref('account.view_move_form').id
        except ValueError:
            pass

        return {
            'name': _('Invoices'),
            'type': 'ir.actions.act_window',
            'domain': [('type', '=', move_type)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'views': [(tree_id, 'tree'),(form_id, 'form')],
            'context': {'default_type': move_type},
        }
