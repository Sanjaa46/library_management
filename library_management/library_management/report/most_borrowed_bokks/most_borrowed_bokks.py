import frappe

def execute(filters=None):
    data = frappe.db.sql("""
        SELECT a.article_name AS book, COUNT(*) AS total_borrowed
        FROM `tabLibrary Transaction` lt
        JOIN `tabArticle` a ON lt.article = a.article_name
        WHERE lt.type = 'Issue'
        GROUP BY a.article_name
        ORDER BY total_borrowed DESC
        LIMIT 10
    """, as_dict=True)

    columns = [
        {"label": "Book", "fieldname": "book", "fieldtype": "Data", "width": 200},
        {"label": "Times Borrowed", "fieldname": "total_borrowed", "fieldtype": "Int", "width": 120},
    ]

    chart = {
        "data": {
            "labels": [row["book"] for row in data],
            "datasets": [{"name": "Borrowed", "values": [row["total_borrowed"] for row in data]}],
        },
        "type": "bar",
    }

    return columns, data, None, chart
