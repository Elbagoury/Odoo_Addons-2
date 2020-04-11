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

from odoo import http
from odoo.http import request
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)

class WebsiteAppointment(http.Controller):

    @http.route(['/appointment'], type='http',auth='public' , website=True )
    def _get_appointment_page(self, **kw):
        group_id = request.env['appointment.person.group'].sudo().search([])
        return request.render('website_appointment.book_appoint_mgmt_template',
            {
                'group_id'  :    group_id,
            })

    @http.route(["/find/app/person"], type="json", auth="public", website=True)
    def _get_appoint_person(self, group_id, appoint_date=False):
        app_group_obj = request.env['appointment.person.group'].sudo().search([('id', '=', int(group_id))]) or False
        selected_day = ''
        if appoint_date:
            selected_day = datetime.strptime(str(appoint_date),'%Y-%m-%d').strftime("%A").lower()
        if app_group_obj:
            appoint_person_dict = {}
            for rec in app_group_obj.sudo().appoint_person_ids:
                if selected_day != '':
                    slot_available = rec.time_slot_ids.filtered(lambda o: o.day == selected_day)
                    if slot_available:
                        appoint_person_dict[rec.id] = rec.name
                else:
                    appoint_person_dict[rec.id] = rec.name
            return appoint_person_dict

    @http.route(["/check/multi/appointment"], type="json", auth="public", website=True)
    def _check_multi_appointments(self, appoint_date, time_slot_id, appoint_person_id):
        appoint_person_obj = request.env["res.partner"].browse(appoint_person_id)
        time_slot_id = request.env["appointment.timeslot"].browse(time_slot_id)
        if appoint_person_obj and time_slot_id and not appoint_person_obj.allow_multi_appoints:
            appointment_obj = request.env["appointment"].search([
                ("appoint_date",'=', appoint_date),
                ("appoint_person_id",'=', appoint_person_obj.id),
                ("time_slot","=", time_slot_id.id),
            ])
            if appointment_obj:
                return False
        return True

    @http.route(["/find/appointee/timeslot"], type="json", auth="public", website=True)
    def _get_appoint_person_date_timeslots(self, group_id, appoint_date):

        if appoint_date:
            dt = appoint_date
            d1 = datetime.strptime(dt,"%Y-%m-%d").date()
            d2 = date.today()
            rd = relativedelta(d2,d1)
            if rd.days > 0 or rd.months > 0 or rd.years > 0:
                return

        app_group_obj = request.env['appointment.person.group'].sudo().search([('id', '=', int(group_id))])
        selected_day = datetime.strptime(str(appoint_date),'%Y-%m-%d').strftime("%A").lower()
        vals = {
            'app_group_obj' : app_group_obj.sudo() ,
            'selected_day': selected_day,
        }
        # if person_id:
        #     vals = {
        #         'app_group_obj' : app_group_obj.sudo() ,
        #         'selected_day': selected_day,
        #         'person_id': request.env['res.partner'].sudo().search([('id','=',int(person_id))]),
        #     }
        return request.env['ir.ui.view'].render_template('website_appointment.appointee_listing_template', vals)

    @http.route("/appointment/book", type="http", auth="public", website=True )
    def _book_appointment(self, **appoint_dict):
        if appoint_dict=={}:
            return request.redirect("/appointment")
        customer = request.env.user.partner_id
        appoint_group = request.env['appointment.person.group'].sudo().search([('id', '=', int(appoint_dict.get('appoint_groups', False)))])
        appoint_person = request.env['res.partner'].sudo().search([('id', '=', int(appoint_dict.get('appoint_person', False)))])
        appoint_date = appoint_dict.get('appoint_date', False)
        appoint_slot = request.env['appointment.timeslot'].sudo().search([('id', '=', int(appoint_dict.get('appoint_timeslot_id', False)))])

        appoint_charge = 0
        if appoint_person and appoint_person.appoint_person_charge > 0:
            appoint_charge = appoint_person.appoint_person_charge
        else:
            if appoint_group and appoint_group.group_charge > 0:
                appoint_charge = appoint_group.group_charge

        vals = {
            'customer': customer,
            'appoint_group':appoint_group,
            'appoint_person': appoint_person,
            'appoint_date': appoint_date,
            'appoint_slot': appoint_slot,
            'appoint_charge': appoint_charge,
        }
        if appoint_dict.get('appoint_error'):
            vals.update({
                'appoint_error' : appoint_dict.get('appoint_error'),
            })
        return request.render('website_appointment.confirm_book_appoint_mgmt_template', vals)

    @http.route("/appointment/confirmation", type="http", auth="public", website=True )
    def _confirm_appointment(self, **post):
        if post == {}:
            return request.redirect("/appointment")
        try:
            customer = request.env.user.partner_id
            appoint_group = request.env['appointment.person.group'].sudo().search([('id', '=', int(post.get('appoint_group', False)))])
            appoint_person = request.env['res.partner'].sudo().search([('id', '=', int(post.get('appoint_person', False)))])
            appoint_date = post.get('appoint_date', False)
            appoint_slot = request.env['appointment.timeslot'].sudo().search([('id', '=', int(post.get('appoint_slot', False)))])
            source = request.env.ref('wk_appointment.appoint_source3')
            vals = {
                'customer': customer.id,
                'appoint_group_id': appoint_group.id,
                'appoint_person_id': appoint_person.id,
                'appoint_date': appoint_date,
                'time_slot': appoint_slot.id,
                'source': source.id if source else False,
                'appoint_state': 'new',
                'description' : post.get("appoint_desc", False) if post.get("appoint_desc") else ''
            }
            appoint_obj = request.env['appointment'].sudo().create(vals)

            appoint_charge = 0
            name = ""
            if appoint_person and appoint_person.appoint_person_charge > 0:
                appoint_charge = appoint_person.appoint_person_charge
                name = "Charge for Appointment Person"
            else:
                if appoint_group and appoint_group.group_charge > 0:
                    appoint_charge = appoint_group.group_charge
                    name = "Charge for Appointment Group"
            if appoint_charge > 0:
                appoint_line = {
                    'appoint_product_id': appoint_group.product_tmpl_id.product_variant_id.id if appoint_group else False,
                    'tax_id': [(6, 0, appoint_group.product_tmpl_id.product_variant_id.taxes_id.ids)],
                    'appoint_id': appoint_obj.id,
                    'name': name,
                    'price_unit': appoint_charge,
                }
                appoint_lines = request.env['appointment.lines'].sudo().create(appoint_line)
            else:
                appoint_line = {
                    'appoint_product_id': appoint_group.product_tmpl_id.product_variant_id.id if appoint_group else False,
                    'tax_id': [(6, 0, appoint_group.product_tmpl_id.product_variant_id.taxes_id.ids)],
                    'appoint_id': appoint_obj.id,
                    'name': "Appointment Free of Charge",
                    'price_unit': 0.0,
                    'product_qty' : 1.0,
                    'price_subtotal': 0.0,
                }
                appoint_lines = request.env['appointment.lines'].sudo().create(appoint_line)
        except:
            return request.redirect(request.httprequest.referrer + "?appoint_error=1")
        return request.redirect("/my/appointments/" + str(appoint_obj.id))
