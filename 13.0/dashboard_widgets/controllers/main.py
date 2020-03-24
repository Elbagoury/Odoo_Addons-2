import odoo.http as http
from odoo.http import request


class DashboadWidgetsHelper(http.Controller):

    @http.route('/dashboard/html/<int:widget_id>', type='http', auth='user', website=True)
    def dashboard_widget_html(self, widget_id, **kwargs):
        widget = request.env['is.dashboard.widget'].browse(widget_id).exists()
        if not widget:
            widget = request.env['is.dashboard.widget.preview'].browse(widget_id).exists()
        if widget and widget.html:
            return widget.html
        else:
            return 'Please save record first to preview'

    @http.route('/dashboard/render_data/<int:widget_id>', type='http', auth='user', website=True)
    def dashboard_render_data(self, widget_id, **kwargs):
        widget = request.env['is.dashboard.widget'].browse(widget_id).exists()

        if widget.display_mode == 'graph':
            render_type = 'chart'
            data = widget.dashboard_data
        else:
            render_type = 'html'
            data = widget.render_dashboard_markup

        return {
            'render_type': render_type,
            'data': data,
        }
