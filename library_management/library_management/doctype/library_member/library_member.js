frappe.ui.form.on('Library Member', {
    refresh(frm) {

        frm.add_custom_button('Create Transaction', () => {
            frappe.new_doc('Library Transaction', { library_member: frm.doc.name });
        });
    }
});
