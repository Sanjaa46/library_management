frappe.pages['test_page'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Test Page',
		single_column: true
	});

	// Load template HTL into the page
	$(frappe.render_template("test_page", {})).appendTo(page.body);

	frappe.call({
        method: "library_management.api.get_stripe_publishable_key",
        callback: function(r) {
            if (r.message && r.message.publishable_key) {
                const stripe = Stripe(r.message.publishable_key);

                $('#pay_now').on('click', function() {
                    frappe.call({
                        method: "library_management.library_management.page.test_page.test_page.create_checkout_session",
                        callback: function(res) {
                            if (res.message && res.message.sessionId) {
                                stripe.redirectToCheckout({
                                    sessionId: res.message.sessionId
                                });
                            }
                        }
                    });
                });
            } else {
                frappe.msgprint("Stripe publishable key not found.");
            }
        }
    });
}