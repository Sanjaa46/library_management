# Copyright (c) 2025, Sanjaa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class LibraryMember(Document):
	
	# this method will run every time a document is saved
	def before_save(self):
		self.full_name = f'{self.first_name} {self.last_name or ""}'
		
		
		
		
	def validate(self):
		exists = frappe.db.exists(
			"Library Member",
			{
				"email_address": self.email_address

			}
		)

		if exists:
			frappe.throw("Email is already exists!")