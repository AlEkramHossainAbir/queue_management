from odoo import api, fields, models


class Officer(models.Model):
    _name = 'queue.officer'
    # _rec_name = 'name'
    _description = 'Queue Officer'

    fieldB = fields.Many2one('queue.token', string='Field B', compute="_compute_states")
    category = fields.Char()

    def _compute_states(self):
        result = self.env['queue.token'].search([('state', '=', 'draft')])[0]
        self.fieldB = result
        self.category = result.category.category

    def solved_state(self):
        self.fieldB.state = 'solved'

