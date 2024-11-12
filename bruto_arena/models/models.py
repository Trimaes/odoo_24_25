# -*- coding: utf-8 -*-

from odoo import models, fields, api
#Jugadores
class player(models.Model):
    _name = 'bruto_arena.player'
    _description = 'Players'

    name = fields.Char()
    #Relation
    characters = fields.One2many(string='Characters', comodel_name='bruto_arena.character', inverse_name='player')
#Personajes
class character(models.Model):
    _name = 'bruto_arena.character'
    _description = 'Characters'

    name = fields.Char()
    level = fields.Integer()
    experience = fields.Integer()
    health = fields.Integer()
    strength = fields.Integer()
    agility = fields.Integer()
    speed = fields.Integer()
    resistance = fields.Integer()
    #Relations
    player = fields.Many2one(string='Player', comodel_name='bruto_arena.player')
    skills = fields.Many2many(comodel_name='bruto_arena.skill',
                              relation='character_skills',
                              column1='character_name',
                              column2='character_skills')

    weapons = fields.Many2many(comodel_name='bruto_arena.weapon',
                              relation='character_weapons',
                              column1='character_name',
                              column2='character_weapons')

    pets = fields.Many2many(comodel_name='bruto_arena.pet',
                              relation='character_pets',
                              column1='character_name',
                              column2='character_pets')

    mounts = fields.Many2many(comodel_name='bruto_arena.mount',
                              relation='character_mounts',
                              column1='character_name',
                              column2='character_mounts')
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
    interval = fields.Integer()
    reach = fields.Integer()
    reversal_rate = fields.Integer() #Contraataque 
    combo_rate = fields.Integer()
    disarm_rate = fields.Integer()
    precision = fields.Integer()
    evasion = fields.Integer()
    block_rate = fields.Integer()
    accuracy = fields.Integer()

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

