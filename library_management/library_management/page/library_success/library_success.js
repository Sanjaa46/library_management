frappe.pages['library-success'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Payment Success',
		single_column: true
	});
}