from odoo import api, fields, models

class CounterManager(models.Model):
    _name = 'counter.manager'
    _rec_name = 'counter_manager_name'
    _description = 'Counter Manager'

    counter_manager_name = fields.Char(string="Name")

