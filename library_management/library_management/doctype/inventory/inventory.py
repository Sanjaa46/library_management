# Copyright (c) 2025, Sanjaa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Inventory(Document):
	def on_update(self):
		article = frappe.get_doc("Article", self.article)
		article.status = "Issued" if self.quantity == 0 else "Available"
		article.save()