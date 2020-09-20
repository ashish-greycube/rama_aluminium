frappe.ui.form.on('Quotation', {
    after_save: function (frm) {
            frappe.call({
                method: 'rama_aluminium.api.quotation_calculate_price_by_weight',
                args: {
                    'doc': frm.doc,
                },
                async: false,
                callback: (r) => {
                    console.log(r)
                    frm.reload_doc()
                },
                error: (r) => {
                    // on error
                }
            })
    }
});

frappe.ui.form.on('Quotation Item', {

    item_code: function (frm, cdt, cdn) {
        if (frm.doc.calculate_price_by_weight_cf === 1) {
            let row = locals[cdt][cdn];
            if (row.item_code) {
                frappe.db.get_value('Item', row.item_code, 'length_cf')
                    .then(r => {
                        let length_cf = r.message.length_cf;
                        row.length_cf = length_cf;
                    })
                frappe.db.get_value('Item', row.item_code, 'weight_per_unit')
                    .then(r => {
                        let catalog_meter_weight_cf = r.message.weight_per_unit;
                        row.catalog_meter_weight_cf = catalog_meter_weight_cf;
                       
                    })
                    setTimeout(function () {
                        row.price_cf = row.rate
                        row.total_weight_cf=row.length_cf*row.qty*row.catalog_meter_weight_cf
                        frm.refresh_field("items");
                    }, 200)                    
            }
        } else if (frm.doc.calculate_price_by_weight_cf === 0) {
            let row = locals[cdt][cdn];
            if (row.item_code) {
                setTimeout(function () {
                    row.price_cf = row.rate
                    row.total_weight_cf= row.total_weight
                    frm.refresh_field("items");
                }, 200)

                frappe.db.get_value('Item', row.item_code, 'weight_per_unit')
                    .then(r => {
                        let catalog_meter_weight_cf = r.message.weight_per_unit;
                        row.catalog_meter_weight_cf = catalog_meter_weight_cf;
                    })
            }
        }

    },
    rate: function (frm, cdt, cdn) {
            let row = locals[cdt][cdn];
            if (row.rate && row.price_cf==0) {
                row.price_cf = row.rate
            }
    },
    qty: function (frm, cdt, cdn) {
            let row = locals[cdt][cdn];
            if (row.qty) {
                if (frm.doc.calculate_price_by_weight_cf === 1) {
                    row.total_weight_cf=row.length_cf*row.qty*row.catalog_meter_weight_cf
                    frm.refresh_field("items")           
                }else if (frm.doc.calculate_price_by_weight_cf === 0) {
                    row.total_weight_cf=row.qty*row.catalog_meter_weight_cf
                    frm.refresh_field("items")                   
                }

            }
    }
})