frappe.ui.form.on('Library Member', {
    refresh: function (frm) {
        // Only load Stripe once
        if (!window.Stripe) {
            let s = document.createElement('script');
            s.src = 'https://js.stripe.com/v3/';
            s.onload = () => {
                console.log('Stripe.js loaded');
            };
            document.head.appendChild(s);
        }

        // payment button logic
        if (frm.doc.payment_status !== 'Paid') {
            // Add Stripe Elements card input if not already added
            if (!document.getElementById('card-element')) {
                let div = document.createElement('div');
                div.id = 'card-element';
                div.style.marginTop = '10px';
                frm.fields_dict['full_name'].wrapper.appendChild(div);

                let error_div = document.createElement('div');
                error_div.id = 'card-errors';
                error_div.style.color = 'red';
                frm.fields_dict['full_name'].wrapper.appendChild(error_div);
            }

            frm.add_custom_button('Pay Membership Fee', async () => {
                // Dynamically load Stripe.js if not loaded
                if (!window.Stripe) {
                    await new Promise((resolve) => {
                        let s = document.createElement('script');
                        s.src = 'https://js.stripe.com/v3/';
                        s.onload = resolve;
                        document.head.appendChild(s);
                    });
                }

                const stripe = Stripe('pk_test_51SFU29Gxhse6wQviiQWRUfi7M9WBk9of1QRe2dHq4sYx7n5qArSBNN4aHtWLiH5UCdEk2IiK2et7OXXpf9CfnYmR00YsKATJ0Q');
                const elements = stripe.elements();
                const card_element = elements.create('card');
                card_element.mount('#card-element');

                // Call backend to create PaymentIntent
                const r = await frappe.call({
                    method: 'library_management.api.create_membership_payment',
                    args: { member_name: frm.doc.name }
                });

                const clientSecret = r.message.client_secret;

                // Confirm the payment using card_element
                const result = await stripe.confirmCardPayment(clientSecret, {
                    payment_method: { card: card_element, billing_details: { name: frm.doc.full_name } }
                });

                if (result.error) {
                    frappe.msgprint('Payment failed: ' + result.error.message);
                } else if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
                    // Update Frappe record
                    await frappe.call({
                        method: 'library_management.api.verify_payment',
                        args: {
                            member_name: frm.doc.name,
                            payment_intent_id: result.paymentIntent.id
                        }
                    });
                    frm.reload_doc();
                    frappe.msgprint('Payment successful!');
                }
            });
        }
        frm.add_custom_button('Create Transaction', () => {
            frappe.new_doc('Library Transaction', {
                library_member: frm.doc.name
            })
        })
    }
});
