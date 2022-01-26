from odoo import api, fields, models, _


class AssignToMe(models.Model):
    _name = 'queue.officer_assign'
    # _rec_name = 'name'
    _description = 'Officer Can Assign to themselves'

    counter_num = fields.Many2one('queue.counter', "Counter No", required=True)
    currently_assign = fields.Many2one('res.users', string="Support Engineer", required=True)
    current_token = fields.Many2one('queue.token', string="Current Token", compute="_compute_states")

    def _compute_states(self):
        result = self.env['queue.token'].search([('state', '=', 'draft')])[0]
        self.current_token = result
