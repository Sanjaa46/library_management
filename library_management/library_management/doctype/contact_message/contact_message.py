# Copyright (c) 2025, Sanjaa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ContactMessage(Document):
	def after_insert(self):
		if not self.reply and not self.responded:
			frappe.sendmail(
				# recipients="librarian@example.com"
				recipients="sanjaas880@gmail.com",
				subject="Library member sent message.",
				message=f"You recieved a message from your customer. http://localhost:8000/app/contact-message/{self.name}"
			)


	def on_submit(self):
		if not self.reply:
			frappe.throw("Reply field is required!")

		subject = "Librarian Response to your message"

		frappe.sendmail(
			recipients=self.email_address,
			subject=subject,
			message=self.reply
		)
		self.responded = True

		library_member = frappe.get_value("Library Member", {"email_address": self.email_address})

		if library_member:
			notification = frappe.get_doc({
				"doctype": "Library Notification",
				"library_transaction": "",
				"library_member": library_member,
				"title": "Message response sent.",
				"message": "Librarian has responded to your please message please check your email.",
				"is_read": False,
				"type": "response"
			})
			notification.insert(ignore_permissions=True)

		frappe.db.commit()

		
