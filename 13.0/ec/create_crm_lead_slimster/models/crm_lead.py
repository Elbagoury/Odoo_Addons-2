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
    def slimster_parser(self, emailBody):
        """This Method returns plain text dict for 
        Template slimster
        """
        plain_text_body = tools.html2plaintext(emailBody)
        newdict = {}
        a = find_between_r(plain_text_body, 'Bron', 'Concullega').split('\n')
        if len(a) > 1:
            werkzaamheden = ''
            materiaal = ''
            model = ''
            uitvoermoment = ''
            opdrachtomschrijving = ''
            gespreksverslag = ''
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
            telefoonindex = [i for i, s in enumerate(a) if 'Telefoon:' in s]
            if telefoonindex and telefoonindex[0]:
                telefoon = a[telefoonindex[0]+1].split(' ') 
                newdict['Telefoon:'] = telefoon[0] if len(telefoon) == 2 else ''
            emailindex = [i for i, s in enumerate(a) if 'E-mailadres:' in s]
            if emailindex and emailindex[0]:
                newdict['E-mailadres:'] = a[emailindex[0]+1] or ''
            adresindex = [i for i, s in enumerate(a) if 'Adres:' in s]
            if adresindex and adresindex[0]:
                newdict['Adres:'] = a[adresindex[0]+1] or ''
                city_zip = a[adresindex[0]+2].split(' ')
                newdict['Plaats:'] = city_zip[2] if len(city_zip) == 4 else ''
                newdict['Postcode:'] = str(city_zip[0]+city_zip[1]) if len(city_zip) == 4 else ''
            # lead description
            werkzaamhedenindex = [i for i, s in enumerate(a) if 'Werkzaamheden:' in s]
            if werkzaamhedenindex and werkzaamhedenindex[0]:
                werkzaamhedenValue = a[werkzaamhedenindex[0]+1] or ''
                if werkzaamhedenValue:
                    werkzaamheden = ': '.join(['Werkzaamheden', werkzaamhedenValue])
            materiaalindex = [i for i, s in enumerate(a) if 'Gewenste traprenovatie materiaal:' in s]
            if materiaalindex and materiaalindex[0]:
                materiaalValue = a[materiaalindex[0]+1] or ''
                if materiaalValue:
                    materiaal = ': '.join(['Gewenste traprenovatie materiaal', materiaalValue])
            modelindex = [i for i, s in enumerate(a) if 'Model trap:' in s]
            if modelindex and modelindex[0]:
                modelValue = a[modelindex[0]+1] or ''
                if modelValue:
                    model = ': '.join(['Model trap', modelValue])
            uitvoermomentindex = [i for i, s in enumerate(a) if 'Uitvoermoment:' in s]
            if uitvoermomentindex and uitvoermomentindex[0]:
                uitvoermomentValue = a[uitvoermomentindex[0]+1] or ''
                if uitvoermomentValue:
                    uitvoermoment = ': '.join(['Uitvoermoment', uitvoermomentValue])
            opdrachtomschrijvingindex = [i for i, s in enumerate(a) if 'Opdrachtomschrijving:' in s]
            if opdrachtomschrijvingindex and opdrachtomschrijvingindex[0]:
                opdrachtomschrijvingValue = a[opdrachtomschrijvingindex[0]+1] or ''
                if opdrachtomschrijvingValue:
                    opdrachtomschrijving = ': '.join(['Opdrachtomschrijving', werkzaamhedenValue])
            gespreksverslagingindex = [i for i, s in enumerate(a) if 'Gespreksverslag:' in s]
            if gespreksverslagingindex and gespreksverslagingindex[0]:
                gespreksverslagValue = a[gespreksverslagingindex[0]+1] or ''
                if gespreksverslagValue:
                    gespreksverslag = ': '.join(['Gespreksverslag', gespreksverslagValue])
            # set description
            description = '\n\n'.join(
                [x for x in [werkzaamheden, materiaal, model, uitvoermoment, opdrachtomschrijving, gespreksverslag] if x])
            if description:
                newdict['description:'] = description
        return newdict

    @api.model
    def slimster_condition(self, mailMessage, emailBody):
        """Condition for slimster template."""
        return (mailMessage.company == 'slimster' or
                'slimster' in emailBody)

    @api.model
    def registerCompanyParser(self):
        """Register slimster Parser Mappin in main."""
        parsers = super(crm_lead, self).registerCompanyParser()
        parsers.append(
            (3,
             self.slimster_condition,
             self.slimster_parser)
        )
        return parsers
