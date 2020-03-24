from odoo import api, fields, models


class IsDashboardWidgetTableColumn(models.Model):
    _name = 'is.dashboard.widget.auto_view.column'
    _description = 'Dashboard record list field'
    _order = 'sequence'

    sequence = fields.Integer()
    field_id = fields.Many2one('ir.model.fields', string="Column")
    dashboard_id = fields.Many2one('is.dashboard.widget')
    show_sum = fields.Boolean()
    invisible = fields.Boolean(string="Hide Column")


class IsDashboardWidgetTable(models.Model):
    _inherit = 'is.dashboard.widget'

    open_action_1_auto_generate_view = fields.Boolean()
    open_action_1_auto_generate_action_id = fields.Many2one('ir.actions.act_window', readonly=True, string="Auto-Generated Action")
    open_action_1_auto_generate_tree_view_id = fields.Many2one('ir.ui.view', readonly=True, string="List View")
    open_action_1_auto_generate_form_view_id = fields.Many2one('ir.ui.view', string="Form View")
    open_action_1_auto_generate_view_column_ids = fields.One2many(string="Columns", comodel_name='is.dashboard.widget.auto_view.column', inverse_name='dashboard_id')

    def get_auto_view_action_vals(self):
        return {
            'name': self.name,
            'res_model': self.query_1_config_model_id.model,
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'view_ids': [(5, 0, 0),
                 (0, 0, {'view_mode': 'tree', 'view_id': self.open_action_1_auto_generate_tree_view_id.id}),
                 (0, 0, {'view_mode': 'form', 'view_id': self.open_action_1_auto_generate_form_view_id.id})
             ]
        }

    def get_auto_view_tree_view_vals(self):
        arch = "<tree>\r\n"
        for col in self.open_action_1_auto_generate_view_column_ids:
            arch += "\t<field name=\"{}\" {} {}/>\r\n".format(
                col.field_id.name,
                "sum=\"{}\"".format(col.field_id.field_description) if col.show_sum else "",
                "invisible=\"1\"" if col.invisible else "",
            )
        arch += "</tree>"
        return {
            'name': "{} (List View)".format(self.name),
            'model': self.query_1_config_model_id.model,
            'priority': 99,
            'arch_base': arch,
        }

    def action_update_auto_view(self):
        for rec in self:
            if not rec.open_action_1_auto_generate_view:
                continue

            if not rec.open_action_1_auto_generate_tree_view_id:
                rec.open_action_1_auto_generate_tree_view_id = self.env['ir.ui.view'].sudo().create(rec.get_auto_view_tree_view_vals())
            else:
                rec.sudo().open_action_1_auto_generate_tree_view_id.write(rec.get_auto_view_tree_view_vals())

            if not rec.open_action_1_auto_generate_action_id:
                rec.open_action_1_auto_generate_action_id = self.env['ir.actions.act_window'].sudo().create(rec.get_auto_view_action_vals())
            else:
                rec.sudo().open_action_1_auto_generate_action_id.write(rec.get_auto_view_action_vals())
            rec.action_id = rec.open_action_1_auto_generate_action_id
