from odoo import api, fields, models


class DashboardWidget(models.AbstractModel):
    _inherit = 'is.dashboard.widget.abstract'

    display_mode = fields.Selection(selection_add=[
        ("embed_html", "Embed HTML"),
        ("embed_iframe_html", "Embed HTML (iframe)"),
        ("embed_iframe_url", "Embed URL (iframe)"),
    ])

    html_render_url = fields.Text(compute="compute_html_render_url")
    html = fields.Text(string="HTML")
    iframe_url = fields.Char()

    def compute_html_render_url(self):
        for rec in self:
            rec.html_render_url = '/dashboard/html/{}'.format(rec.id)
