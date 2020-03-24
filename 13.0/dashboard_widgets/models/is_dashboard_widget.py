from odoo import models, fields, api
from datetime import date, datetime

import json
from odoo.addons.web.controllers.main import clean_action
from odoo.tools import frozendict


class DashboardWidgetAbstract(models.AbstractModel):
    _name = 'is.dashboard.widget.abstract'
    _description = "Dashboard Record"
    _order = 'sequence,id'

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer()
    display_mode = fields.Selection(string="Dashboard Type", selection=[('line_break', 'Start New Line')], required=True)
    datasource = fields.Selection(string="Data Source", required=True, selection=[])

    use_cache = fields.Boolean(string="Use Cached results", help="Store a cached copy of the results for faster rendering for slow running queries")
    last_cache_updated_datetime = fields.Datetime(string="Cache Last Updated", readonly=True)

    show_on_global_dashboard = fields.Boolean(string="Show on dashboard", default=False)

    config_id = fields.Many2one(comodel_name="is.dashboard.widget", string="Config")

    group_by_label = fields.Char(string="Group By Label")
    tag_ids = fields.Many2many('is.dashboard.widget.tag', string="Dashboard Tags")

    show_on_partner_dashboard = fields.Boolean(string="Show on partner dashboard")

    action_id = fields.Many2one(string="Action", comodel_name='ir.actions.act_window')

    kanban_class_main = fields.Char(string="Kanban Class Main", compute='_compute_kanban_class_main')

    color = fields.Integer(string='Color Index')

    date_end = fields.Datetime(compute="compute_date_range")
    date_start = fields.Datetime(compute="compute_date_range")

    dashboard_data = fields.Text(compute='compute_dashboard_data')

    hide_dashboard_item = fields.Boolean(string="Hide dashboard Item")
    widget_hidden = fields.Boolean(compute="compute_widget_hidden")

    render_dashboard_markup = fields.Html(compute="compute_render_dashboard_markup", sanitize=False)

    def get_render_data(self):
        return {
            'name': self.name,
            'display_mode': self.display_mode,
            'widget_type': self.widget_type,
        }

    def compute_render_dashboard_markup(self):
        for rec in self:
            rec._setup_render_dashboard_markup_error()
            try:
                rec._compute_kanban_class_count()  # TODO: Done to fix Odoo cache miss error. Can we fix and remove the underlying issue here?

                rec.render_dashboard_markup = self.env['ir.qweb'].render('dashboard_widgets.render_dashboard_widget', values={'record': rec, 'data': rec.get_render_data()})
                errors = rec._get_render_dashboard_markup_errors()
                if errors:
                    rec.render_dashboard_markup = "ERROR: {0}".format(repr(errors))
            except Exception as ex:
                errors = rec._get_render_dashboard_markup_errors()
                if errors:
                    pass
                rec.render_dashboard_markup = "ERROR: {0}".format(repr(ex))

    def _setup_render_dashboard_markup_error(self):
        if isinstance(self.env.context, frozendict):
            self.env.context.render_dashboard_markup_errors = []
        else:
            self.env.context['render_dashboard_markup_errors'] = []

    def _get_render_dashboard_markup_errors(self):
        if isinstance(self.env.context, frozendict) and hasattr(self.env.context, 'render_dashboard_markup_errors'):
            return self.env.context.render_dashboard_markup_errors
        else:
            return self.env.context.get('render_dashboard_markup_errors')

    def _add_render_dashboard_markup_error(self, title, error):
        if isinstance(self.env.context, frozendict):
            if not hasattr(self.env.context, 'render_dashboard_markup_errors'):
                self.env.context.render_dashboard_markup_errors = []
            self.env.context.render_dashboard_markup_errors += (title, error)
        else:
            if 'render_dashboard_markup_errors' not in self.env.context:
                self.env.context['render_dashboard_markup_errors'] = []
            self.env.context['render_dashboard_markup_errors'] += (title, error)

    def get_widget_hidden(self):
        return self.hide_dashboard_item  # Allow override in other functions

    def compute_widget_hidden(self):
        for rec in self:
            rec.widget_hidden = rec.get_widget_hidden()

    def compute_dashboard_data(self):
        for rec in self:
            def converter(o):
                if isinstance(o, datetime):
                    return fields.Datetime.to_string(o)
                elif isinstance(o, date):
                    return fields.Date.to_string(o)
                elif o.__class__.__name__ == 'lazy':
                    return o.__str__()
                raise TypeError("Unable to parse type {}".format(o.__class__.__name__))

            rec.dashboard_data = json.dumps(rec.get_dashboard_data(), default=converter)

    def get_dashboard_data(self):
        pass  # Functionality defined in extension modules

    def compute_date_range(self):
        pass  # Hook in each implementation

    def action_open_data(self):
        pass  # Functionality defined in extension modules

    def action_open_data_segment(self, data):
        if all(x in data for x in ['data_model', 'data_action']):
            model = data['data_model']
            action = data['data_action']
            if action:
                action = self.env['ir.actions.act_window'].browse(action).exists()
            domain = data.get('data_domain', [])
            return self._action_open_data(model=model, action=action, domain=domain)

    @api.depends()
    def _compute_kanban_class_main(self):
        for rec in self:
            rec.kanban_class_main = ''

    def _action_open_data(self, model, action=False, domain=False, **kwargs):
        self.ensure_one()

        if action:
            action = action.read([])[0]
        else:
            action = {
                'name': self.name,
                'type': 'ir.actions.act_window',
                'res_model': model,
                'view_mode': 'tree,form',
            }

        if domain:
            action['domain'] = domain

        return clean_action(action)


class DashboardWidget(models.Model):
    _name = 'is.dashboard.widget'
    _inherit = 'is.dashboard.widget.abstract'
    _description = "Dashboard Record"
