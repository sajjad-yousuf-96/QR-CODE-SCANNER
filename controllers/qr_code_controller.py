# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from collections import defaultdict
from datetime import datetime
from odoo import http, _
from odoo.http import request
from odoo.modules.module import get_resource_path
from odoo.osv import expression
from odoo.tools import pdf, split_every
from odoo.tools.misc import file_open


class StockBarcodeController(http.Controller):

    @http.route('/qr_code_scanner/scan_from_main_menu', type='json', auth='user')
    def main_menu(self, barcode, **kw):
        """ Receive a barcode scanned from the main menu and return the appropriate
            action (open an existing / new picking) or warning.
        """
        barcode_type = None
        data = str(barcode)

        # Split the data into lines
        lines = data.split('\n')

        # Initialize an empty dictionary
        data_dict = {}

        # Iterate through the lines and create key-value pairs
        for line in lines:
            parts = line.split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                data_dict[key] = value
        print(data_dict)
        partner_record_exist = request.env['res.partner'].sudo().search([('nic_id','=',data_dict['ID'])])
        print(partner_record_exist)
        if partner_record_exist:
            return {'warning': _('ID Already Exist %(ID)s with name %(name)s') % {
                'ID': data_dict['ID'],'name':partner_record_exist.name}}

        date_format = '%d/%m/%Y'
        res_partner_record = request.env['res.partner'].sudo().create({
                'nic_id':data_dict['ID'],
                'name':data_dict['Full name'],
                'province_name':data_dict['Province'],
                'issue_province':data_dict['Issue Province'],
                'marital_status':data_dict['Marital status'],
                'gender':'Feminine' if data_dict['Sex'] == 'Feminino' or data_dict['Sex'].title()[0]=="F" else 'Masculine',
                'issue_date':datetime.strptime(data_dict['ID issue date'], date_format),
                'exp_date':datetime.strptime(data_dict['ID Exp date'], date_format),
            }
        )
        # print(res_partner_record,data_dict)
        return res_partner_record.id