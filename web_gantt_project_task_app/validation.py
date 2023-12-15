# -*- coding: utf-8 -*-
import logging
import os

from lxml import etree

from odoo.loglevels import ustr
from odoo.tools import misc, view_validation
from odoo.modules.module import get_resource_path

_logger = logging.getLogger(__name__)

_ganttt_validator = None


@view_validation.validate('ganttt')
def schema_ganttt(arch, **kwargs):
    """ Check the gantt view against its schema

    :type arch: etree._Element
    """
    global _ganttt_validator

    if _ganttt_validator is None:
        with misc.file_open(os.path.join('web_gantt_project_task_app', 'views', 'gantt.rng')) as f:
            base_url = os.path.join(get_resource_path('base', 'rng'), '')
            _ganttt_validator = etree.RelaxNG(etree.parse(f, base_url=base_url))

    if _ganttt_validator.validate(arch):
        return True

    for error in _ganttt_validator.error_log:
        _logger.error(ustr(error))
    return False
