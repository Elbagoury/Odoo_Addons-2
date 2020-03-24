from odoo import api, SUPERUSER_ID
import re


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})


    views = env['ir.ui.view'].with_context(active_test=False).search([
        ('model', 'ilike', 'is.dashboard.widget'),
        ('mig_flag_dashboard', '=', True)
    ])

    if not views:
        # mig_flag_dashboard not available during install (or all views are disable)
        views = env['ir.ui.view'].with_context(active_test=False).search([
            ('model', 'ilike', 'is.dashboard.widget'),
            ('active', '=', False),
        ])
    views.write({'active': True})
