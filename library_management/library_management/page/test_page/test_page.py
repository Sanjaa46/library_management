import frappe
import stripe


@frappe.whitelist(allow_guest=True)
def get_stripe_publishable_key():
    site_config = frappe.get_site_config()
    return {"publishable_key": site_config.get("stripe_publishable_key")}

@frappe.whitelist(allow_guest=True)
def create_checkout_session():
    site_config = frappe.get_site_config()
    stripe.api_key = site_config.get("stripe_secret_key")

    YOUR_DOMAIN = frappe.utils.get_url()  # e.g. http://library.localhost:8000

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": 2000,  # amount in cents (=$20)
                        "product_data": {"name": "Test Product"},
                    },
                    "quantity": 1,
                }
            ],
            success_url=f"{YOUR_DOMAIN}/app/test_page?success=true",
            cancel_url=f"{YOUR_DOMAIN}/app/test_page?canceled=true",
        )

        return {"sessionId": checkout_session.id}
    except Exception as e:
        frappe.log_error(f"Stripe error: {str(e)}", "Stripe Checkout Error")
        frappe.throw("Error creating Stripe checkout session.")