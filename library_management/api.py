import stripe
import frappe
from frappe import _

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
def create_checkout_session(membership, fee_id):
    site_config = frappe.get_site_config()
    stripe.api_key = site_config.get("stripe_secret_key")

    member_name = frappe.get_value("Library Membership", membership, 'library_member')
    member = frappe.get_doc("Library Member", member_name)
    fee = frappe.get_doc("Membership Fee", fee_id)

    session = stripe.checkout.Session.create(
        customer=member.stripe_customer_id,
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "Library Membership Fee"},
                "unit_amount": int(fee.amount * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"{frappe.utils.get_url()}/membership-success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{frappe.utils.get_url()}/membership-cancel",
    )

    return {"sessionId": session.id, "url": session.url}


@frappe.whitelist(allow_guest=True)
def stripe_webhook():
    site_config = frappe.get_site_config()
    stripe.api_key = site_config.get("stripe_secret_key")

    payload = frappe.request.get_data(as_text=True)
    sig_header = frappe.get_request_header("Stripe-Signature")
    endpoint_secret = site_config.get("stripe_webhook_secret")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        frappe.log_error(f"Webhook Error: {str(e)}", "Stripe Webhook")
        frappe.local.response.http_status_code = 400
        return "Invalid webhook"

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        stripe_payment_id = session.get("payment_intent")
        stripe_customer_id = session.get("customer")

        # Find member by Stripe customer ID
        member = frappe.get_value("Library Member", {"stripe_customer_id": stripe_customer_id}) # Bat
        print("type of member", type(member))
        if not member:
            frappe.log_error("Member not found for customer_id: " + stripe_customer_id, "Stripe Webhook")
            return "Member not found"

        membership_name = frappe.get_value("Library Membership", {"library_member": member})
        membership = frappe.get_doc("Library Membership", membership_name)
        print(f"Membership: {membership}")
        # Find Membership Fee (latest draft for that member)
        fee = frappe.get_doc("Membership Fee", {"library_membership": membership.name, "status": "Draft"})
        if not fee:
            frappe.log_error("No draft fee found for member: " + member, "Stripe Webhook")
            return "No fee found"
        print(f"Fee: {fee}")
        # Mark fee as paid
        fee.db_set("status", "Paid")
        fee.db_set("stripe_payment_id", stripe_payment_id)
        fee.db_set("payment_date", frappe.utils.nowdate())

        membership.db_set("from_date", frappe.utils.nowdate())
        membership.db_set("paid", 1)


    return "Success"


