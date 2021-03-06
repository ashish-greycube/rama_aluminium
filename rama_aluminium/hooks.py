# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "rama_aluminium"
app_title = "Rama Aluminium"
app_publisher = "GreyCube Technologies"
app_description = "Customization for Aluminium Product Manufacturing Company"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/rama_aluminium/css/rama_aluminium.css"
# app_include_js = "/assets/rama_aluminium/js/rama_aluminium.js"

# include js, css files in header of web template
# web_include_css = "/assets/rama_aluminium/css/rama_aluminium.css"
# web_include_js = "/assets/rama_aluminium/js/rama_aluminium.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
"Quotation":"public/js/quotation.js",
"Sales Order":"public/js/sales_order.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "rama_aluminium.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "rama_aluminium.install.before_install"
# after_install = "rama_aluminium.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "rama_aluminium.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Stock Entry": {
		"on_submit": "rama_aluminium.api.update_job_order_CT_packed_qty",
		"on_cancel": "rama_aluminium.api.update_job_order_CT_packed_qty"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"rama_aluminium.tasks.all"
# 	],
# 	"daily": [
# 		"rama_aluminium.tasks.daily"
# 	],
# 	"hourly": [
# 		"rama_aluminium.tasks.hourly"
# 	],
# 	"weekly": [
# 		"rama_aluminium.tasks.weekly"
# 	]
# 	"monthly": [
# 		"rama_aluminium.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "rama_aluminium.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "rama_aluminium.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
override_doctype_dashboards = {
	"Serial No": "rama_aluminium.config.serial_no_dashboard.get_data",
	"Sales Order": "rama_aluminium.config.sales_order_dashboard.get_data"
}

