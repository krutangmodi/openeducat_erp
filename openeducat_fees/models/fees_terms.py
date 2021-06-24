# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, api, fields, exceptions, _


class OpFeesTermsLine(models.Model):
    _name = 'op.fees.terms.line'
    _rec_name = 'due_days'

    due_days = fields.Integer('Due Days')
    value = fields.Float('Value (%)')
    fees_element_line = fields.One2many("op.fees.element",
                                        "fees_terms_line_id", "Fees Elements")
    fees_id = fields.Many2one('op.fees.terms', 'Fees')


class OpFeesTerms(models.Model):
    _name = "op.fees.terms"
    _inherit = "mail.thread"
    _description = "Fees Terms For Course"

    name = fields.Char('Fees Terms', required=True)
    active = fields.Boolean('Active', default=True)
    note = fields.Text('Description')
    no_days = fields.Integer('No of Days')
    day_type = fields.Selection([('before', 'Before'), ('after', 'After')],
                                'Type')
    line_ids = fields.One2many('op.fees.terms.line', 'fees_id', 'Terms')

    @api.model
    def create(self, vals):
        res = super(OpFeesTerms, self).create(vals)
        if not res.line_ids:
            raise exceptions.AccessError(_("Fees Terms must be Required!"))
        total = 0.0
        for line in res.line_ids:
            if line.value:
                total += line.value
        if total != 100.0:
            raise exceptions.AccessError(_("Fees terms must be divided \
            as such sum up in 100%"))
        return res
