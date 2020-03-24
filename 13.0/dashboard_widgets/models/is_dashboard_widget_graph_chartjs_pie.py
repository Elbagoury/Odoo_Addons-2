from odoo import api, fields, models

from collections import OrderedDict


class DashboardWidgetGraph(models.AbstractModel):
    _inherit = 'is.dashboard.widget.abstract'
