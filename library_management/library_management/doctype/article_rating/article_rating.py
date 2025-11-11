# Copyright (c) 2025, Sanjaa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ArticleRating(Document):

	def validate(self):
		exists = frappe.db.exists(
			"Article Rating",
			{
				"library_member": self.library_member,
				"article": self.article

			}
		)
		if exists:
			frappe.throw("You already wrote review on this book!")



	def after_insert(self):
		self.compute_rating()

		frappe.publish_realtime(
			'new_review',
			{'book': self.article, 'rating': self.rating, 'review': self.review, 'library_member': self.library_member}
		)

	def after_delete(self):
		self.compute_rating()
	
	def compute_rating(self):
		# update rating of article
		article = frappe.get_doc("Article", self.article)
		print(article)
		all_ratings = frappe.get_all("Article Rating", filters={"article": self.article}, fields=["rating"])
		count = len(all_ratings)

		total = sum(int(r["rating"]) for r in all_ratings)
		avg = total / count if count else 0

		article.rating = avg
		article.save(ignore_permissions=True)
	
