frappe.ui.form.on("Article", {
	refresh(frm) {
        if (frm.doc.status === "Available") {
            const user_email = frappe.session.user

            frappe.call({
                method: "library_management.api.has_active_issue",
                args: {
                    book: frm.doc.name
                },
                callback: function(r) {
                    if (!r.message) {
                        frm.add_custom_button("Issue", () => {
                            frappe.call({
                                method: "library_management.api.issue_book",
                                args: {
                                    user_email: user_email,
                                    book: frm.doc.name
                                },
                                callback: function(r) {
                                    if (r.message) {
                                        window.location.href = r.message.url;
                                    }
                                }
                            });
                        });
                    } else {
                        console.log("User already has an active issue for this book")
                    }
                }
            });
            
        };

        // frm.add_custom_button('Set Quantity', () => {
        //     frappe.new_doc('Inventory', { article: frm.doc.name });
        // });
	},
});
