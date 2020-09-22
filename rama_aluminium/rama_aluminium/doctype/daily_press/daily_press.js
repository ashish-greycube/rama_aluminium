// Copyright (c) 2020, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Press', {
	refresh: function(frm) {
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Job Order'),
				function() {
					debugger
					erpnext.utils.map_current_doc({
						method: "rama_aluminium.api.make_job_order",
						source_doctype: "Job Order CT",
						target: frm,
						setters: [
							{
								label: "Customer",
								fieldname: "customer",
								fieldtype: "Link",
								options: "Customer",
								default: frm.doc.customer || undefined
							}
						],
						get_query_filters: {
							docstatus: 0
						}
					})
				}, __("Get items from"));
		}
	}
});
