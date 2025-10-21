import stripe
import frappe
from frappe import _
from .auth import require_auth

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
@require_auth
def get_books(status=None):
    filters = {}
    if status:
        filters["status"] = status

    data = frappe.get_all("Article", fields=["article_name", "author", "status", "image"], filters=filters)
    return {"data": data}

@frappe.whitelist(methods=["GET"], allow_guest=True)
@require_auth
def search(query=None, page=1, page_size=12):
    if not query:
        return {"result": 0, "total": 0, "page": page, "page_size": page_size}
    
    # convert page parameters to int
    page = int(page)
    page_size = int(page_size)
    offset = (page - 1) * page_size

    # Search Articles where title matches query
    results = frappe.db.get_all(
        "Article",
        filters={"article_name": ["like", f"%{query}%"]},
        limit_start=offset,
        limit_page_length=page_size
    )
    

    # Count total matches
    total = frappe.db.count("Article", filters=[["article_name", "like", f"%{query}%"]])

    return {
        "results": results,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }

@frappe.whitelist(methods=["GET"], allow_guest=True)
@require_auth
def book_info(article_name=None):
    if not article_name:
        frappe.throw("Enter book name!")

    book = frappe.get_doc("Article", article_name)
    
    if not book:
        frappe.throw("Book not found!")

    data = {
        "article_name": book.article_name,
        "author": book.author,
        "description": book.description,
        "isbn": book.isbn,
        "status": book.status,
        "image": book.image
    }

    return data

@frappe.whitelist(methods=["GET"], allow_guest=True)
@require_auth
def my_books():
    user_email = frappe.local.user
    user = frappe.get_value("Library Member", {"email_address": user_email})

    books = frappe.get_all(
        "Library Transaction",
        filters={
            "type": "Issue",
            "library_member": user
        },
        fields=["article"],
        pluck='article'
    )

    return {
        "books": books
    } 



@frappe.whitelist(allow_guest=True)
@require_auth
def profile():
    user_email = frappe.local.user
    print(user_email)

    user = frappe.get_all("Library Member", filters={"email_address": user_email}, fields={"name", "first_name", "last_name", "phone", "email_address"})[0]
    print(user)

    data = {
        "id": user.name,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "email": user.email_address
    }

    return data

@frappe.whitelist(methods=["POST"], allow_guest=True)
@require_auth
def change_password(old_password, new_password):
    user_email = frappe.local.user

    # change_password method raises an exception not boolean!
    try:
        frappe.utils.password.check_password(user_email, old_password)
    except:
        frappe.throw("Old password is incorrect", frappe.AuthenticationError)
    
    
    frappe.utils.password.update_password(user_email, new_password)

    return {"Success": True, "message": "Password updated successfully!"}

@frappe.whitelist(methods=['POST'], allow_guest=True)
def forgot_password(email=None):
    if not email:
        frappe.throw("Email is required!")

    if not frappe.db.exists("User", email, cache=True):
        frappe.throw("User not found!")

    if not frappe.db.exists("Library Member", {"email_address": email}):
        frappe.throw("User is not Library member!")

    
    recipient_name = frappe.get_all(
        "Library Member",
        filters={"email_address": email},
        fields={"full_name"},
        pluck="full_name"
    )

    new_reset_token = frappe.generate_hash()

    user = frappe.get_doc("User", email)
    user.last_reset_password_key_generated_on = frappe.utils.now_datetime()
    user.reset_password_key = new_reset_token
    user.save(ignore_permissions=True)
    frappe.db.commit()
    
    subject = "PASSWORD RESET LINK"
    frappe.sendmail(
        # recipients=email,
        recipients="sanjaas880@gmail.com", #temporary email
        subject=subject,
        template='reset_password_email',
        args=dict(
            company_logo="http://library.localhost:8000/files/logo.png",
            company_name="LMS Library",
            user_name=recipient_name[0],
            reset_url=f"http://frontend-url:3000/reset-password?token={new_reset_token}",
            expiration_time=1,
            current_year=frappe.utils.getdate().year,
            contact_email="temphomes880@gmail.com",
            website_url="http://library.localhost:8000",
        )
    )

    return {"Success": True, "message": "Password reset link sent!"}

@frappe.whitelist(methods=["POST"], allow_guest=True)
def reset_password(token, new_password):
    if not frappe.db.exists("User", {"reset_password_key": token}):
        frappe.throw("Invalid link!")

    user_email = frappe.get_all(
        "User",
        filters={"reset_password_key": token},
        pluck="name"
    )[0]

    user = frappe.get_doc("User", user_email)

    now = frappe.utils.now_datetime()
    time_diff = now - user.last_reset_password_key_generated_on
    if not time_diff.total_seconds() < 3600:
        frappe.throw("Reset link expired!")

    user.reset_password_key = None
    user.save(ignore_permissions=True)

    frappe.utils.password.update_password(user_email, new_password)
    frappe.db.commit()

    return {"Success": True, "message": "Password reseted succesfully!"}


@frappe.whitelist(methods=['GET'], allow_guest=True)
@require_auth
def create_checkout_session():
    site_config = frappe.get_site_config()
    stripe.api_key = site_config.get("stripe_secret_key")

    user_email = frappe.local.user
    

    try:
        members = frappe.get_all(
            "Library Member",
            filters={"email_address": user_email},
            fields=['name', 'full_name', 'stripe_customer_id']
        )

        member = members[0]

        if not member:
            frappe.throw("No Library member found with your email!")

        amount = frappe.get_single_value("Library Settings", "membership_fee")

        if not amount:
            frappe.throw("Membership fee is not set in Library settings!")

        membership = frappe.get_doc({
            "doctype": "Library Membership",
            "library_member": member.name,
            "full_name": member.full_name,
        })
        membership.insert(ignore_permissions=True)

        fee = frappe.get_doc({
            "doctype": "Membership Fee",
            "library_membership": membership.name,
            "amount": amount,
            "status": "Draft"
        })
        fee.insert(ignore_permissions=True)

        frappe.db.commit()
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error creating membership: {str(e)}")
        frappe.throw("Failed to create membership. Please try again.")

    print("customer id: ", member.stripe_customer_id)

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
    print(endpoint_secret)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        frappe.log_error(f"Webhook Error: {str(e)}", "Stripe Webhook")
        frappe.local.response.http_status_code = 400
        return "Invalid webhook"

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        stripe_payment_id = session.get("payment_intent")
        frappe.log_error("Stripe payment id: ", stripe_payment_id)
        stripe_customer_id = session.get("customer")

        # Find member by Stripe customer ID
        member = frappe.get_value("Library Member", {"stripe_customer_id": stripe_customer_id})
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


    return "Success"
