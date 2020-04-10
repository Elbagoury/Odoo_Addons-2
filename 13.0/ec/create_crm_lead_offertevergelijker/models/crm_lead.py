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
    def offertevergelijker_parser(self, emailBody):
        """This Method returns plain text dict for
        Template offertevergelijker.
        """
        plain_text_body = tools.html2plaintext(emailBody)
        newdict = {}
        # lead details
        a = find_between_r(plain_text_body, 'Klant gegevens', 'Zijn er nog vragen?').split('\n')
        if len(a) > 1:
            emailindex = [i for i, s in enumerate(a) if 'Email:' in s]
            if emailindex and emailindex[0]:
                finalemailindex = emailindex[0] + 1
                newdict['E-mail:'] = a[finalemailindex]
            telephoneindex = [i for i, s in enumerate(a) if 'Telefoon:' in s]
            if telephoneindex and telephoneindex[0]:
                finaltelephone = telephoneindex[0] + 1
                newdict['Telefoon:'] = a[finaltelephone]
            if a[1]:
                naam = ' '.join(a[1].split())
                newdict['Naam:'] = naam
            if a[2]:
                newdict['Straatnaam:'] = ' '.join(a[2].split())
            if a[3]:
                addressstring = a[3].split(' ')
                if len(addressstring) > 2:
                    newdict['Postcode:'] = addressstring[0]
                    newdict['Plaats:'] = addressstring[-1]
        # lead description
        descText = find_between_r(
            plain_text_body, 'Traprenovatie offerte details', 'Informatie / Opmerking').split('\n')
        if len(descText) > 1:
            huidige = ''
            gewenste = ''
            model = ''

            huidigeindex = [i for i, s in enumerate(descText) if 'Huidige trapbekleding' in s]
            if huidigeindex and huidigeindex[0]:
                huidigeValue = descText[huidigeindex[0]+1] or ''
                if huidigeValue:
                    huidige = ': '.join(['Huidige trapbekleding', huidigeValue])
            gewensteindex = [i for i, s in enumerate(descText) if 'Gewenste trapbekleding' in s]
            if gewensteindex and gewensteindex[0]:
                gewensteValue = descText[gewensteindex[0]+1] or ''
                if gewensteValue:
                    gewenste = ': '.join(['Huidige trapbekleding', gewensteValue])
            modelindex = [i for i, s in enumerate(descText) if 'Model trap' in s]
            if modelindex and modelindex[0]:
                modelValue = descText[modelindex[0]+1] or ''
                if modelValue:
                    model = ': '.join(['Model trap', modelValue])
            # set description
            description = '\n\n'.join([x for x in [huidige, gewenste, model] if x])
            if description:
                newdict['description:'] = description
        return newdict

    @api.model
    def offertevergelijker_condition(self, mailMessage, emailBody):
        """Condition for offertevergelijker template."""
        return (mailMessage.company == 'offertevergelijker' or
                'offertevergelijker' in emailBody)

    @api.model
    def registerCompanyParser(self):
        """Register offertevergelijker Parser Mappin in main."""
        parsers = super(crm_lead, self).registerCompanyParser()
        parsers.append(
            (4,
             self.offertevergelijker_condition,
             self.offertevergelijker_parser)
        )
        return parsers
