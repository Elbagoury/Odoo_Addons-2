# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Job Portal - Online Job application',
    'category': 'website',
    'license': 'LGPL-3',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'https://www.serpentcs.com',
    'summary': """Job Portal for Employer and Job Seeker.
    Online recruitment portal online applicant job recruitment
    website career page Online resume submission
    """,
    'version': '13.0.1.0.0',
    'description': """Job Portal for Employer and Job Seeker.
    Online recruitment portal online applicant job recruitment
    website career page Online resume submission
    """,
    'depends': ['website_hr_recruitment'],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/post_resume_view.xml',
        'views/my_profile.xml',
        'views/res_company.xml',
        'views/hr_employee.xml',
        'views/hr_children.xml',
        'views/hr_applicant.xml',
        'views/hr_job_view.xml',
        'views/res_partner.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False,
    'application': False,
    'price': 99,
    'currency': 'EUR',
}
