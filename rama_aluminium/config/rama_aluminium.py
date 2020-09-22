from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Main Flow"),
			"items": [
				{
					"type": "doctype",
					"name": "Quotation",
					"description": _("Quotes to Leads or Customers."),
				},
				{
					"type": "doctype",
					"name": "Sales Order",
					"description": _("Confirmed orders from Customers."),
				},                
				{
					"type": "doctype",
					"name": "Job Order CT",
                    "label": _("Job Order"),
					"description":_("Job Order"),
				},
				{
					"type": "doctype",
					"name": "Daily Press",
                    "label": _("Daily Press"),
					"description":_("Daily Press"),
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
				}
			]
		},
		{
			"label": _("Support Flow"),
			"items": [
				{
					"type": "doctype",
					"name": "Item",
					"description":_("Item"),
				},
				{
					"type": "doctype",
					"name": "Serial No",
					"description":_("Serial No"),
				}                               

			]
		},
        {
			"label": _("Settings"),
			"items": [
				{
					"type": "doctype",
					"name": "Company",
					"description":_("Company"),
				},
				{
					"type": "doctype",
					"name": "Manufacturing Settings",
					"description": _("Global settings for all manufacturing processes."),
				}                
			]
		}
	]