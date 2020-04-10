# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
#                                                                            #
##############################################################################

from odoo import api, tools, models


def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        return s[start:s.rindex(last, start)]
    except ValueError:
        return ""


class crm_lead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def trapoffertes_parser(self, emailBody):
        """This Method returns plain text dict for 
        Template trapoffertes
        """
        plain_text_body = tools.html2plaintext(emailBody)
        newdict = {}
        a = find_between_r(plain_text_body, 'Opdracht:', 'Offerte details:').split('\n')
        if len(a) > 1:
            # lead details
            naamindex = [i for i, s in enumerate(a) if 'Naam:' in s]

            if naamindex and naamindex[0]:
                if 'Mevr' in a[naamindex[0]+1]:
                    titleMevrouw = self.env.ref('create_crm_lead.res_partner_title_mevrouw')
                    newdict['title'] = titleMevrouw.id if titleMevrouw else False
                elif 'Dhr' in a[naamindex[0]+1]:
                    titleHeer = self.env.ref('create_crm_lead.res_partner_title_heer')
                    newdict['title'] = titleHeer.id if titleHeer else False
                else:
                    titleFamilie = self.env.ref('create_crm_lead.res_partner_title_familie')
                    newdict['title'] = titleFamilie.id if titleFamilie else False
                naam = a[naamindex[0]+1].split('.')
                if len(naam) > 1:
                    newdict['Naam:'] = naam[1]
                else:
                    newdict['Naam:'] = a[naamindex[0]+1] or ''
            adresindex = [i for i, s in enumerate(a) if 'Adres:' in s]
            if adresindex and adresindex[0]:
                adresVal = a[adresindex[0]+1].split('(')
                newdict['Adres:'] = adresVal[0] if len(adresVal) > 1 else ''
            postcodeindex = [i for i, s in enumerate(a) if 'Postcode:' in s]
            if postcodeindex and postcodeindex[0]:
                newdict['Postcode:'] = a[postcodeindex[0]+1] or ''
            plaatsindex = [i for i, s in enumerate(a) if 'Plaats:' in s]
            if plaatsindex and plaatsindex[0]:
                newdict['Plaats:'] = a[plaatsindex[0]+1] or ''
            telefoonindex = [i for i, s in enumerate(a) if 'Telefoon:' in s]
            if telefoonindex and telefoonindex[0]:
                newdict['Telefoon:'] = a[telefoonindex[0]+1] or ''
            emailindex = [i for i, s in enumerate(a) if 'E-mail:' in s]
            if emailindex and emailindex[0]:
                newdict['E-mail:'] = a[emailindex[0]+1] or ''

        return newdict

    @api.model
    def trapoffertes_condition(self, mailMessage, emailBody):
        """Condition for trapoffertes template."""
        return (mailMessage.company == 'trapoffertes' or
                'trapoffertes' in emailBody)

    @api.model
    def registerCompanyParser(self):
        """Register trapoffertes Parser Mappin in main."""
        parsers = super(crm_lead, self).registerCompanyParser()
        parsers.append(
            (5,
             self.trapoffertes_condition,
             self.trapoffertes_parser)
        )
        return parsers
