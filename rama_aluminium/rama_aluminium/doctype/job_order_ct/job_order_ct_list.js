frappe.listview_settings['Job Order CT'] = {
	add_fields: ["status"],
	get_indicator: function(doc)
	{
		if(doc.status == "Draft") {
			return [__("Draft"), "blue", "status,=,Draft"];
		}
		else if(doc.status == "Completed") {
			return [__("Completed"), "green", "status,=,Completed"];
		}
		else if(doc.status == "In Process") {
			return [__("In Process"), "orange", "status,=,In Process"];
		}
		else if(doc.status == "Canceled") {
			return [__("Canceled"), "red", "status,=,Canceled"];
		}
	}
};