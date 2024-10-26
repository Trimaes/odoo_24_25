# -*- coding: utf-8 -*-

from odoo import models, fields, api
#Jugadores
class player(models.Model):
    _name = 'bruto_arena.player'
    _description = 'Players'

    name = fields.Char()
#Personajes
class character(models.Model):
    _name = 'bruto_arena.character'
    _description = 'Characters'

    name = fields.Char()
    health = fields.Integer()
    strength = fields.Integer()
    agility = fields.Integer()
    speed = fields.Integer()
    resistance = fields.Integer()
#Habilidades
class skill(models.Model):
    _name = 'bruto_arena.skill'
    _description = 'Skills'

    name = fields.Char()
    type = fields.Char()
    odds = fields.Float()
    skill_description = fields.Text()
#Armas
class weapon(models.Model):
    _name = 'bruto_arena.weapon'
    _description = 'Weapons'
    #Stats visibles:
    name = fields.Char()
    type = fields.Char()
    damage = fields.Integer()
    odds = fields.Float() #Probabilidad de que se use el arma en combate
    #Boost:
#    interval = fields.Integer()
#    reach = fields.Integer()
#    reversal_rate = fields.Integer() #Contraataque 
#    combo_rate = fields.Integer()
#    disarm_rate = fields.Integer()
#    precision = fields.Integer()
#    evasion = fields.Integer()
#    block_rate = fields.Integer()
#    accuracy = fields.Integer()

#Armadura
#class armor(models.Model):
#    _name = 'bruto_arena.armor'
#    _description = 'Armor'
    #Stats visibles:
#    name = fields.Char()
#    weapon_description = fields.Text()
#    armor = fields.Integer()
#    Bonus:
#    interval = fields.Integer()
#    reversal_rate = fields.Integer() #Contraataque 
#    evasion = fields.Integer()
#    block_rate = fields.Integer()

#Mascotas
class pet(models.Model):
    _name = 'bruto_arena.pet'
    _description = 'Pets'

    name = fields.Char()
    health = fields.Integer()
    damage = fields.Integer()
    agility = fields.Integer()
    speed =  fields.Integer()
    combo_rate = fields.Integer()
    evasion = fields.Integer()
    initiative = fields.Integer()

    pet_description = fields.Text()
#Monturas
class mount(models.Model):
    _name = 'bruto_arena.mount'
    _description = 'Mounts'

    name = fields.Char()
    #Añadir boost
    mount_description = fields.Text()

#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

