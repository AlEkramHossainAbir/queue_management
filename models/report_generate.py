from odoo import api, fields, models


class Report(models.Model):
    _name = 'queue.report'
    _description = 'Report Generate'

    token_no = fields.Many2one('queue.token', string="Current Token")
    counter_no = fields.Many2one('queue.counter', string="Counter No")
    datetime = fields.Datetime(string="Date")
    engineer = fields.Many2one('counter.manager', string="Assigned Officer")
