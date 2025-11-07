import frappe

def check_overdue_books():
    # loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
    # frappe.utils.add_to_date(b["date"], days=loan_period)
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
    trx = frappe.get_doc("Library Transaction", transaction.name)
    member = frappe.get_doc("Library Member", trx.library_member)
    book = frappe.get_doc("Article", trx.article)
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
        recipients="sanjaas880@gmail.com", # temporary email
        subject=subject,
        message=message
    )

overdue = frappe.get_all(
        "Library Transaction",
        filters={
            "type": "Issue",
            "date": ["<", frappe.utils.getdate()]
        },
        fields=["name", "article", "library_member", "date"]
    )

send_overdue_email(overdue[0])