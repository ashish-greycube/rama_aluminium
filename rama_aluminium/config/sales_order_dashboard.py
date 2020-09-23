from __future__ import unicode_literals
from frappe import _

def get_data(data):
	non_standard_fieldnames=data['non_standard_fieldnames']
	non_standard_fieldnames['Job Order CT']='sales_order_reference'
	data['non_standard_fieldnames']=non_standard_fieldnames 

	transactions=data['transactions']
	transactions[3].update({'label': _('Manufacturing'),
				'items': ['Work Order', 'Job Order CT']})
	data['transactions']=transactions
	return data