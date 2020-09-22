# -*- coding: utf-8 -*-
# Copyright (c) 2020, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext import get_default_company

class DailyPress(Document):
	def on_submit(self):
		self.make_stock_entry()

	def make_stock_entry(self):
		fg_warehouse=frappe.db.get_single_value('Manufacturing Settings', 'default_fg_warehouse')
		
		item_defaults = get_item_defaults('1001-07',get_default_company())
		source_warehouse=item_defaults.item_defaults[0].default_warehouse


		work_order = frappe.get_doc("Work Order", work_order_id)
		if not frappe.db.get_value("Warehouse", work_order.wip_warehouse, "is_group") \
				and not work_order.skip_transfer:
			wip_warehouse = work_order.wip_warehouse
		else:
			wip_warehouse = None

		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.purpose = 'Manufacture'
		stock_entry.work_order = work_order_id
		stock_entry.company = work_order.company
		stock_entry.from_bom = 1
		stock_entry.bom_no = work_order.bom_no
		stock_entry.use_multi_level_bom = work_order.use_multi_level_bom
		stock_entry.fg_completed_qty = qty or (flt(work_order.qty) - flt(work_order.produced_qty))
		if work_order.bom_no:
			stock_entry.inspection_required = frappe.db.get_value('BOM',
				work_order.bom_no, 'inspection_required')

		if purpose=="Material Transfer for Manufacture":
			stock_entry.to_warehouse = wip_warehouse
			stock_entry.project = work_order.project
		else:
			stock_entry.from_warehouse = wip_warehouse
			stock_entry.to_warehouse = work_order.fg_warehouse
			stock_entry.project = work_order.project

		stock_entry.set_stock_entry_type()
		stock_entry.get_items()
		return stock_entry.as_dict()