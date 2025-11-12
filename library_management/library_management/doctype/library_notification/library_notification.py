# Copyright (c) 2025, Sanjaa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryNotification(Document):
	def after_insert(self):
		user_email = frappe.get_value("Library Member", self.library_member, "email_address")
		frappe.publish_realtime(
			'new_notification',
			{"name": self.name, 'title': self.title, 'message': self.message}
		)
