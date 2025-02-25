# -*- coding: utf-8 -*-
#from odoo import http


#class MyController(http.Controller):
 #   @http.route('/school/course', auth='user', type='json')
  #  def course(self):
   #     return {
    #        'html':"""
     #           <div id="newschool_banner">
      #              <link href="/newschool/static/src/css/banner.css"
       #                 rel="stylesheet">
        #            <h1>Curs</h1>
         #           <p>Creació de cursos:</p>
          #          <a class="course_button" type="action" data-reload-on-close="true" role="button" data-method="action_course_wizard" data-model="newschool.course_wizard">
           #         Crear curs
            #        </a>
                #</div>
                #"""
        #}


# class Newschool(http.Controller):
#     @http.route('/newschool/newschool', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/newschool/newschool/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('newschool.listing', {
#             'root': '/newschool/newschool',
#             'objects': http.request.env['newschool.newschool'].search([]),
#         })

#     @http.route('/newschool/newschool/objects/<model("newschool.newschool"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('newschool.object', {
#             'object': obj
#         })
