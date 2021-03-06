# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import models, fields, api, _
import logging
import json,ast
from datetime import datetime, timedelta
from babel.dates import format_datetime, format_date
from odoo import models, api, _, fields
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools.misc import formatLang
from lxml import etree
_logger = logging.getLogger(__name__)

class AppointmentDashboard(models.Model):
    _name = "appointment.dashboard"
    _order = "sequence ASC"
    _description = "Appointment Dashboard"

    @api.one
    def _kanban_dashboard_graph(self):
        self.kanban_dashboard_graph = json.dumps(self.get_appoint_dashboard_datas())

    @api.one
    def _kanban_dashboard(self):
        self.kanban_dashboard = json.dumps(self.get_additional_appoint_values())

    kanban_dashboard = fields.Text(compute='_kanban_dashboard')
    kanban_dashboard_graph = fields.Text(compute='_kanban_dashboard_graph')
    color = fields.Integer(string='Color Index')
    name = fields.Char(string="Name", translate=True)
    sequence = fields.Integer("Sequence")
    state = fields.Selection([
        ('new', 'New'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('done','Done')
    ], string="State")
    count_new_appoint = fields.Integer(compute='_get_new_appoint_count')
    count_pending_appoint = fields.Integer(compute='_get_pending_appoint_count')
    count_approved_appoint = fields.Integer(compute='_get_approved_appoint_count')
    count_rejected_appoint = fields.Integer(compute='_get_rejected_appoint_count')
    count_done_appoint = fields.Integer(compute='_get_done_appoint_count')

    @api.multi
    def _get_new_appoint_count(self):
        for rec in self:
            obj = self.env['appointment'].search([('appoint_state', '=', 'new')])
            rec.count_new_appoint = len(obj)

    @api.multi
    def _get_pending_appoint_count(self):
        for rec in self:
            obj = self.env['appointment'].search([('appoint_state', '=', 'pending')])
            rec.count_pending_appoint = len(obj)

    @api.multi
    def _get_approved_appoint_count(self):
        for rec in self:
            obj = self.env['appointment'].search([('appoint_state', '=', 'approved')])
            rec.count_approved_appoint = len(obj)

    @api.multi
    def _get_rejected_appoint_count(self):
        for rec in self:
            obj = self.env['appointment'].search([('appoint_state', '=', 'rejected')])
            rec.count_rejected_appoint = len(obj)

    @api.multi
    def _get_done_appoint_count(self):
        for rec in self:
            obj = self.env['appointment'].search([('appoint_state', '=', 'done')])
            rec.count_done_appoint = len(obj)

    @api.multi
    def open_action(self):
        """return action based on type for related appointment states"""
        action_name = self._context.get('action_name', False)
        if not action_name:
            if self.state == 'new':
                action_name = 'appoint_mgmt_new_appoint_dashboard_action'
            elif self.state == 'pending':
                action_name = 'appoint_mgmt_pending_appoint_dashboard_action'
            elif self.state == 'approved':
                action_name = 'appoint_mgmt_approved_appoint_dashboard_action'
            elif self.state == 'rejected':
                action_name = 'appoint_mgmt_rejected_appoint_dashboard_action'
            elif self.state == 'done':
                action_name = 'appoint_mgmt_done_appoint_dashboard_action'
            else:
                action_name = 'appoint_mgmt_all_appointment_action'
        ctx = self._context.copy()
        ctx.update({})
        [action] = self.env.ref('wk_appointment.%s' % action_name).read()
        action['context'] = ctx
        use_domain = self._context.get('use_domain',[])
        if use_domain:
            if use_domain == 'not_invoiced':
                action['domain'] = ast.literal_eval(action['domain']) + [('invoice_id','=',False)]
            if use_domain == 'invoice_to_validate':
                action['domain'] = ast.literal_eval(action['domain']) + [('invoice_id','!=',False),('invoice_status','=','draft')]
            if use_domain == 'invoice_unpaid':
                action['domain'] = ast.literal_eval(action['domain']) + [('invoice_id','!=',False),('invoice_status','=','open')]
            if use_domain == 'invoice_paid':
                action['domain'] = ast.literal_eval(action['domain']) + [('invoice_id','!=',False),('invoice_status','=','paid')]
        return action

    @api.multi
    def action_create_new(self):
        return {
            'name': _('Create Appointment'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': "appointment",
            'view_id': self.env.ref('wk_appointment.appoint_mgmt_book_appointment_form_view').id,
            'context': {'default_appoint_date':str(fields.Date.today())},
        }

    @api.multi
    def get_appoint_dashboard_datas(self):
        data = []
        today = datetime.strptime(str(fields.Date.context_today(self)), DF)
        data.append({'label': _('Past'), 'value':0.0, 'type': 'past'})
        day_of_week = int(format_datetime(today, 'e', locale=self._context.get('lang') or 'en_US'))
        first_day_of_week = today + timedelta(days=-day_of_week+1)
        for i in range(-1,4):
            if i==0:
                label = _('This Week')
            elif i==3:
                label = _('Future')
            else:
                start_week = first_day_of_week + timedelta(days=i*7)
                end_week = start_week + timedelta(days=6)
                if start_week.month == end_week.month:
                    label = str(start_week.day) + '-' +str(end_week.day)+ ' ' + format_date(end_week, 'MMM', locale=self._context.get('lang') or 'en_US')
                else:
                    label = format_date(start_week, 'd MMM', locale=self._context.get('lang') or 'en_US')+'-'+format_date(end_week, 'd MMM', locale=self._context.get('lang') or 'en_US')
            data.append({'label':label,'value':0.0, 'type': 'past' if i<0 else 'future'})

        # Build SQL query to find amount aggregated by week
        select_sql_clause = """SELECT sum(amount_total) as total, min(appoint_date) as aggr_date from appointment where appoint_state = %(appoint_state)s"""
        query = ''
        start_date = (first_day_of_week + timedelta(days=-7))
        for i in range(0,6):
            if i == 0:
                query += "("+select_sql_clause+" and appoint_date < '"+start_date.strftime(DF)+"')"
            elif i == 5:
                query += " UNION ALL ("+select_sql_clause+" and appoint_date >= '"+start_date.strftime(DF)+"')"
            else:
                next_date = start_date + timedelta(days=7)
                query += " UNION ALL ("+select_sql_clause+" and appoint_date >= '"+start_date.strftime(DF)+"' and appoint_date < '"+next_date.strftime(DF)+"')"
                start_date = next_date

        self.env.cr.execute(query, {'appoint_state':self.state})
        query_results = self.env.cr.dictfetchall()
        for index in range(0, len(query_results)):
            if query_results[index].get('aggr_date') != None:
                data[index]['value'] = query_results[index].get('total')
        return [{'values': data}]

    @api.multi
    def get_additional_appoint_values(self):
        AppointObj = self.env['appointment'].sudo()
        currency = self.env.user.company_id.currency_id
        for rec in self:
            not_invoiced = AppointObj.search([('appoint_state','=',rec.state),('invoice_id','=',False)])
            amount_total_not_invoiced = sum(not_invoiced.mapped('amount_total'))
            invoice_to_validate = AppointObj.search([('appoint_state','=',rec.state),('invoice_id','!=',False),('invoice_status','=','draft')])
            amount_total_invoice_to_validate = sum(invoice_to_validate.mapped('amount_total'))
            invoice_unpaid = AppointObj.search([('appoint_state','=',rec.state),('invoice_id','!=',False),('invoice_status','=','open')])
            amount_total_invoice_unpaid = sum(invoice_unpaid.mapped('amount_total'))
            invoice_paid = AppointObj.search([('appoint_state','=',rec.state),('invoice_id','!=',False),('invoice_status','=','paid')])
            amount_total_invoice_paid = sum(invoice_paid.mapped('amount_total'))
            return {
                'not_invoiced': len(not_invoiced),
                'amount_total_not_invoiced': formatLang(self.env, amount_total_not_invoiced or 0.0, currency_obj=currency),
                'invoice_to_validate': len(invoice_to_validate),
                'amount_total_invoice_to_validate': formatLang(self.env, amount_total_invoice_to_validate or 0.0, currency_obj=currency),
                'invoice_unpaid': len(invoice_unpaid),
                'amount_total_invoice_unpaid': formatLang(self.env, amount_total_invoice_unpaid or 0.0, currency_obj=currency),
                'invoice_paid': len(invoice_paid),
                'amount_total_invoice_paid': formatLang(self.env, amount_total_invoice_paid or 0.0, currency_obj=currency),
            }




    # query for not invoiced appointments
    # query = """SELECT count(id) AS count_rec, sum(amount_total) AS total FROM appointment WHERE appoint_state = %s AND invoice_id IS NULL;"""
    # self.env.cr.execute(query, (rec.state,))
    # query_results = self.env.cr.dictfetchall()
    # amount_total_not_invoiced = query_results[0].get('total')
    # not_invoiced = query_results[0].get('count_rec')

    # query for invoiced appointments
    # query = """SELECT count(id) AS count_rec, sum(amount_total) AS total FROM appointment WHERE appoint_state = %s AND invoice_id IS NOT NULL AND invoice_status = %s;"""
    # self.env.cr.execute(query, (rec.state,'draft'))
    # query_results = self.env.cr.dictfetchall()
    # amount_total_invoice_to_validate = query_results[0].get('total')
    # invoice_to_validate = query_results[0].get('count_rec')
