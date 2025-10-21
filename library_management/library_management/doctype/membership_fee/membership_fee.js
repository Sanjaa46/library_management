/*
frappe.ui.form.on("Membership Fee", {
    refresh(frm) {
        if (frm.doc.status === "Draft") {
            frm.add_custom_button("Pay Membership Fee", () => {
                frappe.call({
                    method: "library_management.api.create_checkout_session",
                    args: {
                        membership: frm.doc.library_membership,
                        fee_id: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            window.location.href = r.message.url;
                        }
                    }
                });
            });
        }
    },
});
*/