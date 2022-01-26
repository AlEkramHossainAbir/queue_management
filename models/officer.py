from odoo import api, fields, models


class Officer(models.Model):
    _name = 'queue.officer'
    # _rec_name = 'name'
    _description = 'Queue Officer'

    token = fields.Many2one('queue.token', 'Token No', compute="_compute_states")
    category = fields.Char("Category")
    current_time = fields.Char('Time')
    solved_token = fields.Char('solved_token', compute="solved_token_compute")

    def _compute_states(self):
        result = self.env['queue.token'].search([('state', '=', 'draft')])[0]
        self.token = result
        self.category = result.category.category
        self.current_time = result.current_date

    def solved_state(self):
        self.token.state = 'solved'

    # def solved_token_compute(self):
    #     result = self.env['queue.token'].search([('state', '=', 'solved')])
    #     for i in result:
    #         self.token = result
    #         print("kjds  ", result[i])
