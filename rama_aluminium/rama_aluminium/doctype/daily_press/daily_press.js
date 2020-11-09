// Copyright (c) 2020, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Press', {
	setup: function (frm) {
		set_filter_on_items_cast_items(frm)
	},
	company: function (frm) {
		set_filter_on_items_cast_items(frm)
	},
	refresh: function (frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__('Job Order'),
				function () {
					erpnext.utils.map_current_doc({
						method: "rama_aluminium.api.make_job_order",
						source_doctype: "Job Order CT",
						target: frm,
						setters: [{
							label: "Customer",
							fieldname: "customer",
							fieldtype: "Link",
							options: "Customer",
							default: frm.doc.customer || undefined
						}],
						get_query_filters: {
							docstatus: 1,
							status:'In Process'
						}
					})
				}, __("Get items from"));
		}
	}
});
frappe.ui.form.on('Daily Press Item', {
	no_of_billets: function (frm, cdt, cdn) {
		set_input_in_kg(frm, cdt, cdn);
	},
	billet_length: function (frm, cdt, cdn) {
		set_input_in_kg(frm, cdt, cdn);
	},
	cast_item: function (frm, cdt, cdn) {
		set_input_in_kg(frm, cdt, cdn);
	},
	actual_weight_per_meter: function (frm, cdt, cdn) {
		set_output_in_kg(frm, cdt, cdn);
	},
	no_of_pcs: function (frm, cdt, cdn) {
		set_output_in_kg(frm, cdt, cdn);
	},
	length: function (frm, cdt, cdn) {
		set_output_in_kg(frm, cdt, cdn);
	},
	test_no_of_billets: function (frm, cdt, cdn) {
		set_test_input(frm, cdt, cdn);
	},
	test_billet_length: function (frm, cdt, cdn) {
		set_test_input(frm, cdt, cdn);
	},
	test_input_in_kg: function (frm, cdt, cdn) {
		set_total_input_in_kg(frm, cdt, cdn);
	},
	input_in_kg: function (frm, cdt, cdn) {
		set_total_input_in_kg(frm, cdt, cdn);
	}
});

function set_test_input(frm,cdt,cdn){
	let row = locals[cdt][cdn];
	if (row.test_no_of_billets !== undefined && row.test_billet_length !== undefined && row.multiplication_factor !== undefined) {
		row.test_input_in_kg = (row.test_no_of_billets * row.test_billet_length * row.multiplication_factor)
		frm.refresh_field('items')
		set_total_input_in_kg(frm, cdt, cdn);
	}	
}

function set_input_in_kg(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	if (row.no_of_billets !== undefined && row.billet_length !== undefined  && row.multiplication_factor !== undefined ) {
		row.input_in_kg = (row.no_of_billets * row.billet_length * row.multiplication_factor)
		frm.refresh_field('items')
		set_total_input_in_kg(frm, cdt, cdn);
	}
}

function set_total_input_in_kg(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	if (row.test_input_in_kg !== undefined && row.input_in_kg !== undefined ) {
		row.total_input_in_kg = (row.test_input_in_kg + row.input_in_kg )
		frm.refresh_field('items')
	}
}

function set_output_in_kg(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	if (row.actual_weight_per_meter !== undefined && row.no_of_pcs !== undefined && row.length !== undefined) {
		row.output_in_kg = (row.actual_weight_per_meter * row.no_of_pcs * row.length)
		frm.refresh_field('items')
	}
}

function set_filter_on_items_cast_items(frm) {
	frappe.db.get_value('Company', frm.doc.company, 'default_raw_material_item_group')
		.then(r => {
			let default_raw_material_item_group = r.message.default_raw_material_item_group
			frm.set_query('cast_item', 'items', () => {
				return {
					filters: {
						item_group: default_raw_material_item_group
					}
				}
			})
		})
}