frappe.ui.form.on('Sales Order', {
    refresh: function (frm) {
        if (frm.doc.docstatus == 1) {
            frm.add_custom_button(__('Job Order'), function () {
                frm.trigger("create_job_order");
            }, __("Create"));

        }
    },
    create_job_order: function (frm) {
        frappe.call({
            method: "rama_aluminium.api.sales_order_create_job_order",
            args: {
                "source_name": cur_frm.doc.name
            },
            freeze: true,
            callback: function (r) {
                if (r.message) {
                        let url_list = '<a href="#Form/Job Order CT/' + r.message.name + '" target="_blank">' + r.message.name + '</a><br>'
                        urlpopup()
                        window.open("#Form/Job Order CT/" + r.message.name)
                        function urlpopup() {
                            frappe.msgprint({
                                title: __('Following Job Order is created'),
                                indicator: 'green',
                                message: __(url_list)
                            })
                        }
                }
            }
        });
    }    

});