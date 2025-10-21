# Copyright (c) 2025, Sanjaa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class LibraryMembership(Document):
	# check before submitting this document
	def before_submit(self):
		loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
		self.to_date = frappe.utils.add_days(self.from_date, loan_period or 30)

	def on_update(self):
		self.submit()

	def after_insert(self):
		new_membership_fee = frappe.get_doc({
			"doctype": "Membership Fee",
			"library_membership": self.name,
			"amount": 10,
			"status": "Draft"
		})
		print(new_membership_fee)

		if frappe.get_user() != "Administrator":
			frappe.set_user("Administrator")
			new_membership_fee.insert(ignore_permissions=True)
			frappe.set_user("Guest")
		
		new_membership_fee.insert()