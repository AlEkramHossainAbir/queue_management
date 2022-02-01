from odoo import api, fields, models


class TokenReport(models.Model):
    _name = 'report.queue_management.report_queue_generate_view'
    _description = "Token Report Generator"

    @api.model
    def _get_report_values(self, docids, data=None):
        print(data)
        return {
            'doc_model': 'queue.token',
            'data': data,
            'docs': self,
        }
