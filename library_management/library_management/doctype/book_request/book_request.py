# Copyright (c) 2025, Sanjaa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BookRequest(Document):
	def before_insert(self):
		exists = frappe.db.exists(
			"Book Request",
			{
				"article": self.article,
				"library_member": self.library_member,
				"docstatus": 0
			}
		)
		if exists:
			frappe.throw("You have already requested this book")


	def on_update(self):
		if not self.library_member:
			user = frappe.session.user
			library_member_name = frappe.get_value("Library Member", {"email_address": user}, "name")
			if library_member_name:
				self.db_set("library_member", library_member_name, update_modified=False)

		if self.status == "Approved" and not self.library_transaction:
			transaction = frappe.get_doc({
				"doctype": "Library Transaction",
				"article": self.article,
				"library_member": self.library_member,
				"type": "Issue",
				"date": frappe.utils.nowdate()
			})
			transaction.insert()
			self.db_set("library_transaction", transaction.name, update_modified=False)
			frappe.log_error(f"Library Transaction {transaction.name} created successfully.")

	
	def on_submit(self):
		if self.status == "Borrowed" and self.library_transaction:
			transaction = frappe.get_doc("Library Transaction", self.library_transaction)
			if transaction.docstatus == 0:
				transaction.submit()
				frappe.log_error(f"Library Transaction {transaction} submitted")
