from __future__ import unicode_literals
from frappe import _

def get_data(data):
	return {
		'fieldname': 'serial_no',
        'non_standard_fieldnames': {
            'Daily Press':'die'
        },      
		'transactions': [
			{
				'items': ['Daily Press']
			},
		]
	}