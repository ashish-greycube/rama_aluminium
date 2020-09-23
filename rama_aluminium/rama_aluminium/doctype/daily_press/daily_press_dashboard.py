from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
        'fieldname': 'daily_press',
		'internal_links': {
			'Job Order CT': ['items', 'job_order'],
            'Serial No':['items', 'die']
		},
		'transactions': [
			{
				'label': _('Reference'),
				'items': ['Job Order CT','Stock Entry']
			}
		]
	}