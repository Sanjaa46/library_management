# Copyright (c) 2025, Sanjaa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BookRequest(Document):
	
	def on_update(self):
		if not self.library_member:
			user = frappe.session.user
			library_member_name = frappe.get_value("Library Member", {"email_address": user}, "name")
			self.library_member = library_member_name
			self.save()

		if self.status == "Approved":
			library_member = self.library_member
			book_name = self.article

			transaction = frappe.get_doc({
				"doctype": "Library Transaction",
				"article": book_name,
				"library_member": library_member,
				"type": "Issue",
				"date": frappe.utils.nowdate()
			})
			transaction.save()
