import frappe

@frappe.whitelist()
def get_books(status=None):

    # Difference between local.user and session.user

    filters = {}
    if status:
        filters["status"] = status


    user = frappe.session.user
    data = frappe.get_all("Article", fields=["article_name", "author", "status"], filters=filters)
    return {"requested by: ": user, "data": data}

@frappe.whitelist(allow_guest=False)
def get_library_stats():
    total_books = frappe.db.count("Article")
    total_members = frappe.db.count("Library Member")
    total_issued = frappe.db.count("Library Transaction", {"type": "Issue"})

    return {
        "books": total_books,
        "members": total_members,
        "issued": total_issued
    }