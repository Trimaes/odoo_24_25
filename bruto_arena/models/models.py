# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random
from datetime import datetime

#Jugadores
class player(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    #_description = 'Players'

    #name = fields.Char()
    photo = fields.Image(max_width=200, max_height=200)
    state = fields.Selection([('1', 'Player')])
    #Relation
    characters = fields.One2many(string='Characters', comodel_name='bruto_arena.character', inverse_name='player')
    
    #@api.model
    #def create(self, values):
    #   record = super(player, self).create(values)
    # EL WRITE SE HARÍA SOBRE result.write
    #    print("Player created", record.name)
    #    return record
    
    #CONSTRAINTS
    #_sql_constraints = [('name_uniq', 'unique(name)', 'This name already exists')]

#Personajes
class character(models.Model):
    _name = 'bruto_arena.character'
    _description = 'Characters'

    name = fields.Char()
    victories = fields.Integer(readonly=True)
    experience = fields.Integer(readonly=True)
    last_fight_date = fields.Datetime(compute='_last_fight', store=True, readonly=True)
    character_graph = fields.One2many('bruto_arena.character_graph','character')
    state = fields.Selection([('1', 'Player'),('2','Character')])
    xp_boost = fields.Many2one(string="XP Boost", comodel_name='purchase.order')
    
    #CRON
    @api.model
    def update_graph(self):
        characters = self.search([])
        for c in characters:
            character_lvl = c.level
            character_vic = c.victories
            character_name = c.name
            
            self.env['bruto_arena.character_graph'].create({'name':character_lvl, 'victories':character_vic,'chatacter':character_name})
    
    @api.model
    def cron_fight(self):
        characters = self.search([])
        for c in characters:
            c.fight()
            
    
    
    def write(self, values):
        result = super(character, self).write(values)
        
        if self.level < 50:
            new_ranking = self.env['bruto_arena.ranking'].search([('name', '=', 'Plata')], limit=1)
            
        
        if self.level < 70 and self.level >= 50:
            new_ranking = self.env['bruto_arena.ranking'].search([('name', '=', 'Oro')], limit=1)
            
            
        if self.level >= 70:
            new_ranking = self.env['bruto_arena.ranking'].search([('name', '=', 'Diamante')], limit=1)
        
        super(character, self.with_context(bypass_write=True)).write({'ranking': new_ranking.id})
                                                                      
        return result
    
    @api.depends('victories')
    def _last_fight(self):
        for r in self:
            r.last_fight_date = datetime.now()
    
    #action
    def fight(self):
        
        opponent = self.env['bruto_arena.character'].search([])[random.randint(0, 50)]
        for c in self:
            if opponent.id != c.id:
                
                win = random.choice([True, False])
                if win == True:
                    c.victories += 1
                    c.experience += 500
                else:
                    return {'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {'title': 'Found opponent', 'message': 'You lose!'}
                    }

        
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

    #Sube el nivel del PJ a cada 1000 puntos de Xp
    @api.depends('experience')
    def _lvl_up(self):
        for c in self:
            c.level = 1 + (c.experience // 1000)
            if c.level%10 == 0:
                self.unlock_skills()
                
            if c.level%15 == 0:
                self.unlock_weapons()


    #Relations
    player = fields.Many2one(string='Player', comodel_name='res.partner', required=True)
    #player_name = fields.Char(related='player.name')

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
    
    #Modificar many2many
    @api.model
    def unlock_skills(self):
        for c in self:
            new_skill = self.env['bruto_arena.skill'].search([('required_level', '=', c.level)])
            c.skills = [(4, skill.id) for skill in new_skill]
            
    @api.model
    def unlock_weapons(self):
        for c in self:
            new_weapon = self.env['bruto_arena.weapon'].search([('required_level', '=', c.level)])
            c.weapons = [(4, weapon.id) for weapon in new_weapon]
    
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
    required_level = fields.Integer()
    state = fields.Selection([('1', 'Character'),('2','Skill')])
#Armas
class weapon(models.Model):
    _name = 'bruto_arena.weapon'
    _description = 'Weapons'
    #Stats visibles:
    name = fields.Char()
    type = fields.Char()
    damage = fields.Integer()
    odds = fields.Float() #Probabilidad de que se use el arma en combate
    required_level = fields.Integer()
    state = fields.Selection([('1', 'Character'),('2','Weapon')])
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
    state = fields.Selection([('1', 'Character'),('2','Pet')])

#Ranking
class ranking(models.Model):
    _name = 'bruto_arena.ranking'
    _description = 'Ranking'

    name = fields.Char(required=True, readonly=True)
    characters = fields.One2many(string='Characters', comodel_name='bruto_arena.character', inverse_name='ranking')
    state = fields.Selection([('1', 'Character'),('2','Ranking')])
    
#Player graph
class character_graph(models.Model):
    _name = 'bruto_arena.character_graph'
    _description = 'character graph'
    
    name = fields.Integer()
    victories = fields.Integer()
    character = fields.Many2one('bruto_arena.character')

class xp_booster(models.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'    
    
    character = fields.One2many(string="Character", comodel_name='bruto_arena.character', inverse_name='xp_boost')       
    
    #SIN USO
    boost_type = fields.Selection([('1', 'XP x2'), ('2', 'XP x3'), ('3', 'XP x5')])
    #SIN USO
    boost = fields.Char()           
    
