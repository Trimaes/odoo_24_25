# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
import random

class character_wizard(models.TransientModel):
    _name = 'bruto_arena.character_wizard'
    _description = 'bruto_arena.character_wizard'
    
    name = fields.Char()
    player = fields.Many2many('bruto_arena.player_aux', required=True)
    skill_name = fields.Char(string="Skill name")
    weapon_name = fields.Char(string="Weapon name")
    weapon_damage = fields.Integer(string="Weapon damage")
    skills = fields.Many2many('bruto_arena.skill_aux')
    weapons = fields.Many2many('bruto_arena.weapon_aux')

    
    @api.model
    def action_create_character_wizard(self):
        action = self.env.ref('bruto_arena.action_create_character_wizard').read()[0]
        return action
    
    def add_skill(self):
        for c in self:
            c.write({'skills':[(0,0,{'name':c.skill_name})]})
            
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
        
    def add_weapon(self):
        for c in self:
            c.write({'weapons':[(0,0,{'name':c.weapon_name, 'damage':c.weapon_damage})]})
            
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    
    def create_character(self):
        for cw in self:
    
            for c in cw.skills:
                 c.env['bruto_arena.skill'].create({'name':c.name})
                 
            for c in cw.weapons:
                 c.env['bruto_arena.weapon'].create({'name':c.name, 'damage':c.damage})
                 
        character = cw.env['bruto_arena.character'].create({'name':cw.name, 'player': cw.player[0].id, 'skills':[(6,0,cw.skills.ids)], 'weapons':[(6,0,cw.weapons.ids)]})
                 
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'bruto_arena.character',
            'res_id': character.id,
            'view_mode': 'form',
            'target': 'current',
        }
                 
            
class player_aux(models.TransientModel):
    _name = 'bruto_arena.player_aux'
    name = fields.Char()
class skill_aux(models.TransientModel):
    _name = 'bruto_arena.skill_aux'
    name = fields.Char()
class weapon_aux(models.TransientModel):
    _name = 'bruto_arena.weapon_aux'
    name = fields.Char()
    damage = fields.Integer()
                                                                                                      
