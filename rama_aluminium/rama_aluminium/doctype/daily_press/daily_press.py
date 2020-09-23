# -*- coding: utf-8 -*-
# Copyright (c) 2020, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext import get_default_company
from frappe.utils import flt
from frappe import _

class DailyPress(Document):
	def validate(self):
		self.validate_items()

	def on_submit(self):
		self.make_die_entries()
		self.make_stock_entry()
	
	def on_cancel(self):
		self.deduct_die_entries()

	def validate_items(self):
		items=self.get("items")
		for item in items:		
			item.input_in_kg=flt(item.no_of_billets) * flt(item.billet_length) * flt(item.multiplication_factor)
			item.output_in_kg =flt(item.actual_weight_per_meter) * flt(item.no_of_pcs) * flt(item.length)
			if item.output_in_kg > item.input_in_kg:
				frappe.throw(_("Row #{0}, Output is more than Input. This will make scrap negative. Cannot proceed.".format(item.idx))) 

	def make_die_entries(self):
		items=self.get("items")
		for item in items:
			used_for_qty_cf = frappe.db.get_value('Serial No', item.die, 'used_for_qty_cf')
			frappe.db.set_value('Serial No', item.die, 'used_for_qty_cf', flt(used_for_qty_cf+item.output_in_kg))

	def deduct_die_entries(self):
		items=self.get("items")
		for item in items:
			used_for_qty_cf = frappe.db.get_value('Serial No', item.die, 'used_for_qty_cf')
			frappe.db.set_value('Serial No', item.die, 'used_for_qty_cf', flt(used_for_qty_cf-item.output_in_kg))

	def make_stock_entry(self):
		default_scrap_item_cf = frappe.db.get_value('Company', self.company, 'default_scrap_item_cf')
		default_scrap_item_warehouse_cf = frappe.db.get_value('Company', self.company, 'default_scrap_item_warehouse_cf')

		fg_warehouse=frappe.db.get_single_value('Manufacturing Settings', 'default_fg_warehouse')
		
		items=self.get("items")
		for item in items:
			stock_entry = frappe.new_doc("Stock Entry")
			stock_entry.stock_entry_type = 'Manufacture'
			stock_entry.company = self.company
			stock_entry.daily_press=self.name
			stock_entry.daily_press_item_name=item.name
			# raw material entry
			row = stock_entry.append('items', {})
			item_defaults = get_item_defaults(item.cast_item,self.company)
			source_warehouse=item_defaults.item_defaults[0].default_warehouse			
			row.s_warehouse=source_warehouse
			row.item_code=item.cast_item
			row.qty=item.input_in_kg
			row.uom=frappe.db.get_value('Item', item.cast_item, 'stock_uom')
			# finished item entry
			row = stock_entry.append('items', {})
			row.t_warehouse=fg_warehouse
			row.item_code=item.item
			row.qty=item.output_in_kg
			row.uom=frappe.db.get_value('Item', item.item, 'stock_uom')			
			# scrap item entry
			row = stock_entry.append('items', {})
			row.allow_zero_valuation_rate=1
			row.basic_rate=0
			row.t_warehouse=default_scrap_item_warehouse_cf
			row.item_code=default_scrap_item_cf
			row.qty=flt(item.input_in_kg)-flt(item.output_in_kg)
			row.uom=frappe.db.get_value('Item',default_scrap_item_cf, 'stock_uom')			

			stock_entry.insert(ignore_permissions=True)