frappe.pages['library_payment'].on_page_load = function(wrapper) {
	new PageContent(wrapper);
}

PageContent = Class.extend({
	init: function (wrapper) {
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: "Library Payment",
			sigle_column: true,
		});

		this.make();
	},

	make: function () {
		let htmlContent = `
		<h2>This is Library Payment page</h2>
		`;

		$(frappe.render_template( htmlContent, this )).appendTo(this.page.main);
	},
})