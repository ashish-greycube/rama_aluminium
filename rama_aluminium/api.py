from __future__ import unicode_literals
import frappe
from frappe.utils import flt, comma_or, nowdate
from frappe.model.mapper import get_mapped_doc
from frappe import _
from frappe.utils import (flt, getdate, get_url, now,
	nowtime, get_time, today, get_datetime, add_days)

@frappe.whitelist()
def quotation_calculate_price_by_weight(doc):
	doc=frappe._dict(frappe.parse_json(doc))
	quotation= frappe.get_doc('Quotation', doc.name)
	qo_items=quotation.get("items")
	if quotation.calculate_price_by_weight_cf ==1:
		for item in qo_items:
			if item.length_cf== None:
				legnth=frappe.db.get_value('Item', item.item_code, 'length_cf')
				item.length_cf=length
			if item.catalog_meter_weight_cf == None:
				item.catalog_meter_weight_cf=item.weight_per_unit
			item.total_weight_cf=item.length_cf*item.qty*item.catalog_meter_weight_cf
			item.total_weight= item.total_weight_cf
			item.weight_per_unit=item.total_weight_cf/item.qty
			amount=item.total_weight_cf*item.price_cf
			item.rate=amount/item.qty
			item.amount=item.rate*item.qty
		quotation.run_method("calculate_taxes_and_totals")
		quotation.save()
		return 1
	elif quotation.calculate_price_by_weight_cf==0:
		for item in qo_items:
			item.catalog_meter_weight_cf=item.weight_per_unit
			item.total_weight_cf=item.total_weight
			item.price_cf= item.rate
		quotation.run_method("calculate_taxes_and_totals")
		quotation.save()
		return 1        

@frappe.whitelist()
def sales_order_create_job_order(source_name, target_doc=None): 
	if not frappe.has_permission("Job Order CT", "write"):
		frappe.throw(_("Not permitted"), frappe.PermissionError)   

	job_order_list=frappe.db.get_list('Job Order CT',filters={'sales_order_reference': source_name },fields=['name'], limit=1)
	if len(job_order_list)>0:
		frappe.throw(_("Job Order already exist {0}  for this Sales Order.").format("<a href='desk#Form/Job Order CT/{0}'> {0} </a>".format(job_order_list[0]['name'])))

	def set_missing_values(source, target):
		pass

	def update_main(source, target, source_parent):
		target.sales_order_reference=source.name
		target.company=source.company
		target.customer=source.customer
		target.transaction_date=nowdate()

	def update_item(source_doc, target_doc, source_parent):
		target_doc.item = source_doc.item_code
		target_doc.weight=source_doc.weight_per_unit
		target_doc.length = source_doc.length_cf
		target_doc.qty = source_doc.qty
		target_doc.total_weight = source_doc.total_weight


	doc = get_mapped_doc("Sales Order", source_name, {
		'Sales Order': {
			"doctype": "Job Order CT",
			"postprocess": update_main,
			},
			"Sales Order Item": {
				"doctype": "Job Order Item CT",
				"field_map":{
					"item":"item_code",
					"weight":"weight_per_unit",
					"length":"length_cf",
					"qty": "qty",
					"total_weight":"total_weight"
				},
				"postprocess": update_item,                
			}						
	}, target_doc, set_missing_values)
	doc.save()
	return doc     

@frappe.whitelist()
def make_job_order(source_name, target_doc=None):
	def set_missing_values(source, target):
		pass
		# target.run_method("set_missing_values")
		# target.run_method("calculate_taxes_and_totals")

	def update_item(obj, target, source_parent):
		target.from_time=get_datetime()
		target.job_order=source_parent.name
		target.item=obj.item
		target.length=obj.length
		target.job_order_item_name_ct=obj.name



	def update_main_item(source,target,source_parent):
		pass

	doclist = get_mapped_doc("Job Order CT", source_name, {
			"Job Order CT": {
				"doctype": "Daily Press",
				"validation": {
					"docstatus": ["=", 1]
				},
				"postprocess": update_main_item
			},
			"Job Order Item CT": {
				"doctype": "Daily Press Item",
				"postprocess": update_item,
				# "condition": lambda doc: (doc.bom_item_config_cf==None)
			}
		}, target_doc, set_missing_values, ignore_permissions=True)

	# postprocess: fetch shipping address, set missing values

	return doclist    

@frappe.whitelist()
def update_job_order_CT_packed_qty(self,method):
	fg_warehouse=frappe.db.get_single_value('Manufacturing Settings', 'default_fg_warehouse')
	job_order_item_name_ct = frappe.db.get_value('Daily Press Item', self.daily_press_item_name, 'job_order_item_name_ct')
	items=self.get("items")
	for item in items:
		if item.t_warehouse==fg_warehouse and method == "on_submit":
			frappe.db.set_value('Job Order Item CT', job_order_item_name_ct, 'produced_qty', item.qty)
			break
		elif item.t_warehouse==fg_warehouse and method == "on_cancel":
			frappe.db.set_value('Job Order Item CT', job_order_item_name_ct, 'produced_qty', 0)
			break
