# Copyright (c) 2025, Sanjaa and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class Article(WebsiteGenerator):
	def after_insert(self):
		inventory = frappe.get_doc({
			"doctype": "Inventory",
			"article": self.name,
			"quantity": 0
		})
		inventory.insert()
