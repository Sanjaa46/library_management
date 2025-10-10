import frappe

def check_overdue_books():
    overdue = frappe.get_all(
        "Library Transaction",
        filters={
            "type": "Issue",
            "date": ["<", frappe.utils.getdate()]
        },
        fields=["name", "article", "library_member", "date"]
    )

    for trx in overdue:
        frappe.enqueue(
            method="library_management.tasks.send_overdue_email",
            queue="short",
            timeout=60,
            enqueue_after_commit=True,
            transaction=trx
        )



def send_overdue_email(transaction):
    trx = frappe.get_doc("Library Transaction", transaction["name"])
    member = frappe.get_doc("Library Member", trx.library_member)
    book = frappe.get_doc("Article", trx.aritlce)
    subject = f"Overdue Book Reminder: {book.article_name}"
    message = f"""
    Dear {member.first_name},

    Our records show that the book **{book.article_name}** was due on {trx.date}.
    Please return it to the library as soon as possible.

    Thank you,
    Library Management
    """

    frappe.sendmail(
        # recipients=member.email_address,
        recipients="sanjaas880@gmail.com",
        subject=subject,
        message=message
    )