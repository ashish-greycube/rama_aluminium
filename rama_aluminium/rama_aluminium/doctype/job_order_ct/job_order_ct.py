# -*- coding: utf-8 -*-
# Copyright (c) 2020, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class JobOrderCT(Document):
	def on_submit(self):
		self.db_set("status", 'In Process')

	def on_cancel(self):
		self.db_set("status", 'Cancelled')