# Copyright (c) 2025, Sanjaa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
import stripe


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
	
	def after_insert(self):
		""" Create Stripe customer when a new library member is created """
		site_config = frappe.get_site_config()
		stripe.api_key = site_config.get("stripe_secret_key")

		try:
			customer = stripe.Customer.create(
				email=self.email_address,
				name=self.full_name,
			)
			self.db_set("stripe_customer_id", customer.id)
			frappe.logger().info(f"Stripe customer created with ID: {customer.id}")
		except Exception as e:
			frappe.log_error(f"Stripe error: {str(e)}", "Stripe Customer Creation Error")

	def after_delete(self):
		""" Delete library member from User table when member is deleted """

		frappe.delete_doc("User", self.email_address)