# Copyright (c) 2025, Sanjaa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BookRequest(Document):
	def before_save(self):
		user = frappe.session.user
		library_member_name = frappe.get_value("Library Member", {"email_address": user}, "name")
		self.library_member = library_member_name