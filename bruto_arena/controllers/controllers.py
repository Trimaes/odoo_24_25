# -*- coding: utf-8 -*-
# from odoo import http


# class BrutoArena(http.Controller):
#     @http.route('/bruto_arena/bruto_arena', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bruto_arena/bruto_arena/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bruto_arena.listing', {
#             'root': '/bruto_arena/bruto_arena',
#             'objects': http.request.env['bruto_arena.bruto_arena'].search([]),
#         })

#     @http.route('/bruto_arena/bruto_arena/objects/<model("bruto_arena.bruto_arena"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bruto_arena.object', {
#             'object': obj
#         })

