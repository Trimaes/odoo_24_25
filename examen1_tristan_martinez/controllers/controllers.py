# -*- coding: utf-8 -*-
# from odoo import http


# class Examen1TristanMartinez(http.Controller):
#     @http.route('/examen1_tristan_martinez/examen1_tristan_martinez', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/examen1_tristan_martinez/examen1_tristan_martinez/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('examen1_tristan_martinez.listing', {
#             'root': '/examen1_tristan_martinez/examen1_tristan_martinez',
#             'objects': http.request.env['examen1_tristan_martinez.examen1_tristan_martinez'].search([]),
#         })

#     @http.route('/examen1_tristan_martinez/examen1_tristan_martinez/objects/<model("examen1_tristan_martinez.examen1_tristan_martinez"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('examen1_tristan_martinez.object', {
#             'object': obj
#         })

