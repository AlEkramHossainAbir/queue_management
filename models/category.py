from odoo import api, fields, models


class Category(models.Model):
    _name = 'queue.category'
    _rec_name = 'category'
    _description = 'All the category will be saved here'

    category = fields.Char(string="Category")

