from odoo import api, fields, models, _


class QueueToken(models.Model):
    _name = 'queue.token'
    _rec_name = 'token_seq'
    _description = 'Crate Token for queue management system'

    # name = fields.Char(string="Name")
    current_date = fields.Datetime(string="Current Time", default=fields.Datetime.now())
    token_seq = fields.Char(string="Token", required=True,
                            copy=False, readonly=True, index=True,
                            default=lambda self: _('New'))

    state = fields.Selection([
        ('draft', 'Draft'),
        ('solved', 'Solved'),
    ], string='Status', readonly=True, default='draft')

    @api.model
    def create(self, vals_list):
        if vals_list.get('token_seq', _('New')) == _('New'):
            vals_list['token_seq'] = self.env['ir.sequence'].next_by_code('queue.token.sequence') or _('New')

        result = super(QueueToken, self).create(vals_list)
        return result

    category = fields.Many2one('queue.category', string="Category")

    def solved_state(self):
        self.state = 'solved'

    def print_token_report(self, t=None, cat=None):
        data = {
            'model': self._name,
            'ids': self.ids,
            'token_seq': t.token_seq,
            'category': cat,
            'date': t.current_date
        }
        return self.env.ref('queue_management.report_queue_token').report_action(self, data=data)
