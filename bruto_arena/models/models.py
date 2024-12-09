# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random
#Jugadores
class player(models.Model):
    _name = 'bruto_arena.player'
    _description = 'Players'

    name = fields.Char()
    photo = fields.Image(max_width=200, max_height=200)
    #Relation
    characters = fields.One2many(string='Characters', comodel_name='bruto_arena.character', inverse_name='player')
    #CONSTRAINTS
    _sql_constraints = [('name_uniq', 'unique(name)', 'This name already exists')]

#Personajes
class character(models.Model):
    _name = 'bruto_arena.character'
    _description = 'Characters'

    name = fields.Char()
    victories = fields.Integer(readonly=True)
    experience = fields.Integer(readonly=True)
    
    
    #action
    def fight(self):
        for c in self:
            c.victories += 1
    
    #Default/Compute
    def _generate_health_value(self):
        return random.randint(80,95)
    health = fields.Integer(default=_generate_health_value, readonly=True)
    
    def _generate_stats(self):
        print('################ GENERANDO STATS #################')
        return random.randint(1,10)

    strength = fields.Integer(default=_generate_stats, readonly=True)
    agility = fields.Integer(default=_generate_stats, readonly=True)
    speed = fields.Integer(default=_generate_stats, readonly=True)
    resistance = fields.Integer(compute='_generate_resistance', store=True, readonly=True)
    level = fields.Integer(compute='_lvl_up', readonly=True)

    #Computa la resistencia en función de agility, strength y health
    @api.depends('agility', 'strength', 'health')
    def _generate_resistance(self):
        for c in self:
            c.resistance = (c.agility // 5) + (c.strength // 5) + (c.health //10)

    #CSube el nivel del PJ a cada 1000 puntos de Xp
    @api.depends('experience')
    def _lvl_up(self):
        for c in self:
            c.level = 1 + (c.experience // 1000)


    #Relations
    player = fields.Many2one(string='Player', comodel_name='bruto_arena.player', required=True)

    ranking = fields.Many2one(string='Rankings', comodel_name='bruto_arena.ranking')
    
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
    
    #CONSTRAINTS
    _sql_constraints = [('name_uniq', 'unique(name)', 'This name already exists')]
    
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
    block_rate = fields.Integer()

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

    pet_description = fields.Text()

#Ranking
class ranking(models.Model):
    _name = 'bruto_arena.ranking'
    _description = 'Ranking'

    name = fields.Char(required=True, readonly=True)
    characters = fields.One2many(string='Characters', comodel_name='bruto_arena.character', inverse_name='ranking')



#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

