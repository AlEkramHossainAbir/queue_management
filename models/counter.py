from odoo import api, fields, models, _


class Counter(models.Model):
    _name = 'queue.counter'
    _rec_name = 'counter_num_seq'
    _description = 'Counter of a bank'

    counter_num_seq = fields.Char(string="Counter Number", required=True,
                                  copy=False, readonly=True, index=True,
                                  default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('counter_num_seq', _('New')) == _('New'):
            vals['counter_num_seq'] = self.env['ir.sequence'].next_by_code('queue.counter.sequence') or _('New')
        result = super(Counter, self).create(vals)
        return result
