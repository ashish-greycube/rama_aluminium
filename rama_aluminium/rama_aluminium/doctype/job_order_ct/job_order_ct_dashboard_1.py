from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
        'fieldname': 'job_order_ct',
		'non_standard_fieldnames': {
			'Daily Press Item': 'job_order',
		},
		'internal_links': {
			'Daily Press': ['items', 'job_order'],
            
		},
		'transactions': [
			{
				'label': _('Reference'),
				'items': ['Daily Press']
			}
		]
	}