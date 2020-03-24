from odoo import api, SUPERUSER_ID
import re


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    feature_installed_mig_flag_dashboard = False
    try:
        env.cr.execute("select id, mig_flag_dashboard from ir_ui_view where model ILIKE 'is.dashboard%';")
        feature_installed_mig_flag_dashboard = True
    except:
        pass

    if feature_installed_mig_flag_dashboard:
        env.cr.execute("update ir_ui_view set mig_flag_dashboard=TRUE where model ILIKE 'is.dashboard.widget%' and active=TRUE")
    env.cr.execute("update ir_ui_view set active=FALSE where model ILIKE 'is.dashboard.widget%'")
