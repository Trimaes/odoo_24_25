# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

import random

class furgoneta(models.Model):
    _name = 'examen1_tristan_martinez.furgoneta'
    _description = 'examen1_tristan_martinez.furgoneta'
    
    def _generar_matricula(self):
        return random.randint(1000,9999)
    matricula = fields.Integer(default=_generar_matricula, readonly=True)
    
    def _generar_capacidad(self):
        return random.randint(3,10)
    capacidad = fields.Integer(default=_generar_capacidad, readonly=True)
    
    foto = fields.Image()
    
    paquetes_enviados = fields.One2many(
        string='Paquetes envidos',
        comodel_name='examen1_tristan_martinez.paquete',
        inverse_name='furgoneta',
    )
    
    
    
    
class paquete(models.Model):
    _name = 'examen1_tristan_martinez.paquete'
    _description = 'examen1_tristan_martinez.paquete'
    
    def _generar_id_paquete(self):
        return random.randint(10000,99999)
    identificador = fields.Integer(default=_generar_id_paquete, readonly=True)
    
    def _generar_volumen(self):
        return random.randint(1,5)
    volumen = fields.Integer(default=_generar_volumen)
    
    
    furgoneta = fields.Many2one(
        string='Furgoneta de reparto',
        comodel_name='examen1_tristan_martinez.furgoneta',
        ondelete='restrict',
    )
    
    
    viaje = fields.Many2one(
        string='Viaje',
        comodel_name='examen1_tristan_martinez.viaje',
        ondelete='restrict',
    )
    
    
    
class viaje(models.Model):
    _name = 'examen1_tristan_martinez.viaje'
    _description = 'examen1_tristan_martinez.viaje'
    
    def _generar_id_viaje(self):
        return random.randint(10000,99999)
    identificador = fields.Integer(default=_generar_id_viaje)
    conductor = fields.Char()
    
    furgoneta = fields.Many2one(
        string='Furgoneta',
        comodel_name='examen1_tristan_martinez.furgoneta',
        ondelete='restrict',
    )
    
    capacidad_aprov = fields.Integer()
    
    @api.constrains('capacidad_aprov')
    def _check_(self):
        for r in self:
            if r.capacidad_aprov > r.furgoneta.capacidad:
                r.capacidad_aprov = 0
            
    
    
    lista_paquetes = fields.One2many(
        string='Lista de paquetes',
        comodel_name='examen1_tristan_martinez.paquete',
        inverse_name='viaje',
    )
    
# class examen1_tristan_martinez(models.Model):
#     _name = 'examen1_tristan_martinez.examen1_tristan_martinez'
#     _description = 'examen1_tristan_martinez.examen1_tristan_martinez'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

