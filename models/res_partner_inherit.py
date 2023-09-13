from markupsafe import Markup
from werkzeug import urls

from odoo import api, fields, models, _
from odoo.addons.http_routing.models.ir_http import slug, url_for
from odoo.http import request
from odoo.exceptions import ValidationError, UserError

import random
import string
import logging

_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = 'res.partner'

    nic_id = fields.Char('NIC ID',required=True)
    province_name = fields.Char('Province',required=True)
    # sex = fields.Char('Sex',required=True)
    gender = fields.Selection([('Masculine','Masculine'),('Feminine','Feminine')],'Gender',required=True)
    marital_status = fields.Char('Marital Status',required=True)
    issue_date = fields.Date('Issue Date',required=True)
    exp_date = fields.Date('Expiry Date',required=True)
    issue_province = fields.Char('Issue Province',required=True)

