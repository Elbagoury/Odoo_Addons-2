# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models, _
import io
import requests
from lxml import etree, objectify
from xml.etree import ElementTree as ET
from lxml import etree as ElementTree

class sh_snippet_builder(models.Model):
    _name = "sh.snippet.builder"
    _description = "Snippet Builder"
    _order = "id desc"
    
    name = fields.Char(string = "Name", required = True)
    html = fields.Text(string = "HTML")
    css = fields.Text(string="CSS")
    js = fields.Text(string = "JS")
    view_id = fields.Many2one(string = "View", comodel_name="ir.ui.view")
    
    
    def action_noupdate_tmpl(self):
        ir_model_data_obj = self.env['ir.model.data'].sudo()
                
        search_rec = ir_model_data_obj.sudo().search([
            ('module','=','sh_snippet_builder'),
            ('name','=','sh_snippet_builder_snippets'),            
            ], limit = 1)
            
        if search_rec:
            vals = {
            'noupdate'  : True,
                }
            search_rec.sudo().write(vals)
     
    @api.model
    def create(self,vals):
        res = super(sh_snippet_builder,self).create(vals)
                
        view_arch = """<?xml version="1.0"?>
        <t name="Snippet Builder %(id)s" t-name="sh_snippet_builder.sh_snippet_builder_ud_tmpl_%(id)s">
            <section class="sh_snippet_builder_section_user_defined">        
        
        """ % {
            
            'id' : res.id
            }


        if res.js:
            view_arch += res.js
        if res.css:
            view_arch += res.css
        if res.html:
            view_arch += res.html        
        
        view_arch += """
            </section>
        </t>
        """
        
        
        # =================================================
        # Create or Write ir ui view template
        # =================================================        
        
        ir_view_obj = self.env['ir.ui.view']
        name = "sh_snippet_builder_ud_tmpl_" + str(res.id)
        key = "sh_snippet_builder." + name
        ir_view_vals = {
            'name' : res.name,
            'arch': view_arch,
            'key' : key,
            'type': 'qweb',
            'active':True,
            'xml_id' : key,
            'priority': 16, 
            'customize_show': False, 
            'mode': 'primary',            
            }    
        view = ir_view_obj.sudo().search([('key', '=', key)], limit=1)
        if view:
            view.sudo().write(ir_view_vals)
        else:         
            view = ir_view_obj.sudo().create(ir_view_vals)
               
        res.write({
            'view_id' : view.id
            })
        
        # =================================================
        # Create or Write ir ui view template
        # =================================================          
        
        
        # =================================================           
        # Data File ir model data start
        # =================================================   
                
        ir_model_data_obj = self.env['ir.model.data'].sudo()
        name = "sh_snippet_builder_ud_tmpl_" + str(res.id)
                
        data_vals = {
            'module'    : 'sh_snippet_builder',
            'name'      : name,
            'model'     : 'ir.ui.view',
            'noupdate'  : True,
            'res_id'    : view.id,
            'reference' : "ir.ui.view," + str(view.id),
            
            }
        ir_model_data_obj.sudo().create(data_vals)
        
        # =================================================           
        # Data File ir model data end
        # =================================================       
        
        
        
        # =========================================================================           
        # Link custom snippet template in our website.snippets inherited template.
        # =========================================================================   
      
                
        view_website_snippet = ir_view_obj.sudo().search([
            ('key','=','sh_snippet_builder.sh_snippet_builder_snippets')
            ],order='id desc' ,limit=1)
        
        if view_website_snippet and view_website_snippet.arch:
#             xml = ElementTree.fromstring(view_website_snippet.arch)
            
            doc = etree.XML(view_website_snippet.arch)
            for node in doc.xpath("//div[@class='o_panel_body']"):
                new_node = """
               <t t-snippet="%(key)s" 
               t-thumbnail="/sh_snippet_builder/static/src/img/blocks/s_1.png"/>                
                
                """ %{
                    'key' : key
                    }
                new_node = ElementTree.fromstring( new_node )
                node.insert(1, new_node)
                break
                
            view_website_snippet.arch = etree.tostring(doc, encoding='unicode')       
        # =========================================================================           
        # Link custom snippet template in our website.snippets inherited template.
        # =========================================================================                   
                  
        return res
    
    
    @api.model
    def create_sh_builder(self,vals):
        res = super(sh_snippet_builder,self).create(vals)
                
        view_arch = """<?xml version="1.0"?>
        <t name="Snippet Builder %(id)s" t-name="sh_snippet_builder.sh_snippet_builder_ud_tmpl_%(id)s">
            <section class="sh_snippet_builder_section_user_defined">        
        
        """ % {
            
            'id' : res.id
            }


        if res.js:
            view_arch += res.js
        if res.css:
            view_arch += res.css
        if res.html:
            view_arch += res.html        
        
        view_arch += """
            </section>
        </t>
        """
        
        
        # =================================================
        # Create or Write ir ui view template
        # =================================================        
        
        ir_view_obj = self.env['ir.ui.view']
        name = "sh_snippet_builder_ud_tmpl_" + str(res.id)
        key = "sh_snippet_builder." + name
        ir_view_vals = {
            'name' : res.name,
            'arch': view_arch,
            'key' : key,
            'type': 'qweb',
            'active':True,
            'xml_id' : key,
            'priority': 16, 
            'customize_show': False, 
            'mode': 'primary',            
            }    
        view = ir_view_obj.sudo().search([('key', '=', key)], limit=1)
        if view:
            view.sudo().write(ir_view_vals)
        else:         
            try:
                view = ir_view_obj.sudo().create(ir_view_vals)
            except Exception as e:
                res.unlink()
                return {'error' : "Invalid Syntax"}     
               
        res.write({
            'view_id' : view.id
            })
        
        # =================================================
        # Create or Write ir ui view template
        # =================================================          
        
        
        # =================================================           
        # Data File ir model data start
        # =================================================   
                
        ir_model_data_obj = self.env['ir.model.data'].sudo()
        name = "sh_snippet_builder_ud_tmpl_" + str(res.id)
                
        data_vals = {
            'module'    : 'sh_snippet_builder',
            'name'      : name,
            'model'     : 'ir.ui.view',
            'noupdate'  : True,
            'res_id'    : view.id,
            'reference' : "ir.ui.view," + str(view.id),
            
            }
        ir_model_data_obj.sudo().create(data_vals)
        
        # =================================================           
        # Data File ir model data end
        # =================================================       
        
        
        
        # =========================================================================           
        # Link custom snippet template in our website.snippets inherited template.
        # =========================================================================   
      
                
        view_website_snippet = ir_view_obj.sudo().search([
            ('key','=','sh_snippet_builder.sh_snippet_builder_snippets')
            ],order='id desc' ,limit=1)
        
        if view_website_snippet and view_website_snippet.arch:
#             xml = ElementTree.fromstring(view_website_snippet.arch)
            
            doc = etree.XML(view_website_snippet.arch)
            for node in doc.xpath("//div[@class='o_panel_body']"):
                new_node = """
               <t t-snippet="%(key)s" 
               t-thumbnail="/sh_snippet_builder/static/src/img/blocks/s_1.png"/>                
                
                """ %{
                    'key' : key
                    }
                new_node = ElementTree.fromstring( new_node )
                node.insert(1, new_node)
                break
                
            view_website_snippet.arch = etree.tostring(doc, encoding='unicode')       
        # =========================================================================           
        # Link custom snippet template in our website.snippets inherited template.
        # =========================================================================                   
                  
        return res
    
    
    def write(self,vals):
        res = super(sh_snippet_builder,self).write(vals)
        
        ir_view_obj = self.env['ir.ui.view'].sudo()        
        for rec in self:
            
            view_arch = """<?xml version="1.0"?>
            <t name="Snippet Builder %(id)s" t-name="sh_snippet_builder.sh_snippet_builder_ud_tmpl_%(id)s">
                <section class="sh_snippet_builder_section_user_defined">        
            
            """ % {
                
                'id' : rec.id
                }
    
            if rec.js:
                view_arch += rec.js
            if rec.css:
                view_arch += rec.css
            if rec.html:
                view_arch += rec.html        
            
            view_arch += """
                </section>
            </t>
            """  
            
            # =================================================
            # Write ir ui view template
            # =================================================        
            
            name = "sh_snippet_builder_ud_tmpl_" + str(rec.id)
            key = "sh_snippet_builder." + name
            ir_view_vals = {
                'name' : rec.name,
                'arch': view_arch,
                'key' : key,
                'type': 'qweb',
                'active':True,
                'xml_id' : key
                }    
            view = ir_view_obj.search([('key', '=', key)])
            if view:
                view.write(ir_view_vals)
             
        
        return res
        


    def unlink(self):
                    
        ir_model_data_obj = self.env['ir.model.data'].sudo()
        ir_view_obj = self.env['ir.ui.view'].sudo()
        for snippet_record in self:
            
            # =================================================           
            # Remove Data File
            # =================================================   
            name = "sh_snippet_builder_ud_tmpl_" + str(snippet_record.id)
            key = "sh_snippet_builder." + name
                                
            domain = [
                ('name','=',name),
                ('module','=','sh_snippet_builder'),
                ('model','=','ir.ui.view'),
            ]

            ir_model_data = ir_model_data_obj.sudo().search(domain, limit = 1)
            if ir_model_data:
                ir_model_data.unlink()
                
            # =================================================           
            # Remove Data File
            # =================================================              
            


            # =========================================================================           
            # Remove links in website snippet
            # =========================================================================   
                    
            view_website_snippet = ir_view_obj.sudo().search([
                ('key','=','sh_snippet_builder.sh_snippet_builder_snippets')
                ],order='id desc',limit = 1)
            
            if view_website_snippet and view_website_snippet.arch:
                              
                
                doc = etree.XML(view_website_snippet.arch)
                xpath = '//t[@t-snippet="'+ key +'"]' 
                
                for node in doc.xpath(xpath):               
                    node.getparent().remove(node)  
                                    
                view_website_snippet.arch = etree.tostring(doc, encoding='unicode')
            
            # =========================================================================           
            # Remove links in website snippet
            # ========================================================================= 
                
            
            # =================================================
            # Remove ir ui view Qweb 
            # =================================================        
            

            
            domain = [
                ('key','=',key),
                ('type','=','qweb'),
            ]
             
            view = ir_view_obj.search(domain, limit=1)
            if view:
                view.unlink()    
                
            # =================================================
            # Remove ir ui view Qweb 
            # =================================================    
            
                        
        return super(sh_snippet_builder, self).unlink()

