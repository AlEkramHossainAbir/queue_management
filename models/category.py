from odoo import api, fields, models, _


class Category(models.Model):
    _name = 'queue.category'
    _rec_name = 'category'
    _description = 'All the category will be saved here'

    token_seq = fields.Char(string="Token", required=True,
                            copy=False, readonly=True, index=True,
                            default=lambda self: _('New'))

    category = fields.Char(string="Category")

    def create_token(self):
        test = self.env['queue.token']
        t = test.create({'category': self.env['queue.category'].search([('category', 'ilike', self.category)]).id})

        result = test.print_token_report(t, self.category)
        return result
