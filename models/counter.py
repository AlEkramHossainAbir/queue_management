from odoo import api, fields, models, _
from odoo.exceptions import UserError, MissingError, ValidationError


class Counter(models.Model):
    _name = 'queue.counter'
    _rec_name = 'counter_num_seq'
    _description = 'Counter of a bank'

    _sql_constraints = [
        ('currently_assign_uniq', 'unique(currently_assign)', 'Assign perseon must be unique'),
    ]

    counter_num_seq = fields.Char(string="Counter Number", required=True,
                                  copy=False, readonly=True, index=True,
                                  default=lambda self: _('New'))

    currently_assign = fields.Many2one('res.users', string="Support Engineer", required=False)
    current_token = fields.Many2one('queue.token', string="Current Token")
    category = fields.Char("Category")
    state = fields.Char('States', store=False, compute="state_update")
    assign_state = fields.Selection([
        ('online', 'Online'),
        ('offline', 'Offline'),
    ], string='Status', readonly=True, default='offline')

    @api.model
    def create(self, vals):
        if vals.get('counter_num_seq', _('New')) == _('New'):
            vals['counter_num_seq'] = self.env['ir.sequence'].next_by_code('queue.counter.sequence') or _('New')
        result = super(Counter, self).create(vals)
        return result

    # def assign_counter(self):
    #     pass
    #
    # def free_counter(self):
    #     pass

    def assign_counter(self):
        # result = self.env['queue.token'].search([('state', '=', 'draft')])[0]
        # self.current_token = result
        # self.category = result.category.category
        for record in self:
            record.currently_assign = self.env.user
            if record.assign_state == 'online':
                record.assign_state = 'offline'

            else:
                record.assign_state = 'online'
        #     if self.env.user.has_group('queue_system.queue_employee_group') and not record.employee:
        #         record.employee = self.env.user
        #         record.assign_state = 'online'
        #     else:
        #         raise UserError("You don't have permission to do this.")
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }
        # action = self.sudo().env.ref('queue_system.employee_counter_action').read()[0]
        # action['target'] = 'main'
        # return self.view_sorted_counter_for_employee()

    def free_counter(self):
        for record in self:
            print(record.current_token)
            record.currently_assign = False
            record.category = False
            if record.assign_state == 'online':
                record.assign_state = 'offline'

            else:
                record.assign_state = 'online'

        # for record in self:
        #     if record.employee:
        #         if record.token_no:
        #             raise ValidationError("Please Process Current Token First. Then Go Offline")
        #         record.employee = False
        #         record.assign_state = 'offline'
        #     else:
        #         raise UserError("No user is Assigned with this counter")

        # action = self.sudo().env.ref('queue_system.employee_counter_action').read()[0]
        # print(action)
        # action['target'] = 'main'
        # return self.view_sorted_counter_for_employee()
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }

    # def change_assign_status(self):
    #     switch
    #
    # Status
    # for record in self:
    #     if record.currently_assign == self.env.user.id:
    #         if record.assign_state == 'online' and record.current_token:
    #             raise ValidationError("Please Process Current Token First. Then go Offline")
    #         elif record.assign_state == 'online' and not record.current_token:
    #             record.assign_state = 'offline'
    #         else:
    #             record.assign_state = 'online'
    #

    @api.depends('current_token')
    def _compute_states(self):
        result = self.env['queue.token'].search([('state', '=', 'draft')])
        if result:
            result = result[0]
        else:
            result = False
            return result
        self.current_token = result
        self.category = result.category.category

    def solved_state(self):
        result = self._compute_states()
        self.current_token.state = 'solved'
        if result == False:
            raise ValidationError("Your record is too small: ")

    def close_token(self):
        for record in self:
            record.current_token = False

    @api.onchange('current_token')
    def state_update(self):
        for record in self:
            record.state = record.current_token.state
