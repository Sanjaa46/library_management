import stripe
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

@frappe.whitelist(allow_guest=True)
def get_stripe_publishable_key():
    site_config = frappe.get_site_config()
    return {"publishable_key": site_config.get("stripe_publishable_key")}

@frappe.whitelist(allow_guest=True)
def create_payment_intent(amount, currency="usd", description=None):
    import stripe
    stripe.api_key = frappe.conf.get("stripe_secret_key")

    intent = stripe.PaymentIntent.create(
        amount=int(float(amount)*100),
        currency=currency,
        description=description or "Library Payment",
        automatic_payment_methods={"enabled": True},
    )

    return {
        "client_secret": intent.client_secret
    }


@frappe.whitelist()
def create_membership_payment(member_name):
    site_config = frappe.get_site_config()
    stripe.api_key = site_config.get("stripe_secret_key")
    membership_fee = frappe.db.get_single_value("Library Settings", "membership_fee")

    member = frappe.get_doc("Library Member", member_name)
    if not member.stripe_customer_id:
        frappe.throw("Stripe customer not found for this member.")

    intent = stripe.PaymentIntent.create(
        amount=int(membership_fee*100),
        currency="usd",
        customer=member.stripe_customer_id,
        metadata={"member_id": member_name},
        description=f"Membership fee for {member.full_name}",
    )

    return {
        "client_secret": intent.client_secret,
        "payment_intent_id": intent.id
    }

@frappe.whitelist()
def verify_payment(member_id, payment_intent_id):
    site_config = frappe.get_site_config()
    stripe.api_key = site_config.get("stripe_secret_key")

    intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    member = frappe.get_doc("Library Member", member_id)

    if intent.status == "succeeded":
        member.payment_status = "Paid"
        member.stripe_payment_id = payment_intent_id
        member.save(ignore_permissions=True)
        frappe.db.commit()
        return {"status": "success"}
    else:
        member.payment_status = "Failed"
        member.save(ignore_permissions=True)
        frappe.db.commit()
        return {"status": "failed"}
