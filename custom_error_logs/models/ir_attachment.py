# -*- coding: utf-8 -*-
import logging

from contextlib import contextmanager

from odoo import api, models
from odoo.tools.parse_version import parse_version


@contextmanager
def log_level(temp_level):
    """Context manager to override root_logger.level for the scope of the block.

    It can be used to hide expected log messages that are polluting the logs.
    """
    _logger = logging.getLogger()
    orig_level = _logger.level
    _logger.setLevel(temp_level)
    try:
        yield _logger
    finally:
        pass
        _logger.setLevel(orig_level)


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def _file_read(self, fname, bin_size=False):
        """WARNING: !!! Remember to disable this when debugging attachments !!!
        """
        self.env.cr.execute("""
            SELECT latest_version 
            FROM ir_module_module 
            WHERE name = 'base';
        """)
        version = parse_version(self.env.cr.fetchone()[0])
        with log_level(logging.WARNING) as _:
            if int(version[0]) < 14:
                return super()._file_read(fname, bin_size)
            else:
                return super()._file_read(fname)
