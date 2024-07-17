# -*- coding: utf-8 -*-

from odoo import models, fields, api
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

class StatementBank(models.Model):
    _inherit = 'account.bank.statement.line'

    is_from_web = fields.Boolean(default=False)
    payment_id = fields.Many2one('account.payment')





