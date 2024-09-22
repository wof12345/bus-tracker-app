import hashlib
import hmac
import json
import time


def generate_stripe_signature(secret: str, payload: dict) -> str:
    timestamp = int(time.time())

    payload_str = json.dumps(payload)
    signed_payload = f'{timestamp}.{payload_str}'

    signature = hmac.new(
        secret.encode('utf-8'), signed_payload.encode('utf-8'), hashlib.sha256
    ).hexdigest()

    return f't={timestamp},v1={signature}'


def get_checkout_completed_event():
    return {
        'id': 'evt_1J4ZD3P4KnHuV8I2Z3Z6yjls',
        'type': 'checkout.session.completed',
        'data': {
            'object': {
                'id': 'cs_test_a1SrEacsUwdF2dW4PCFiQ1JDJliOgYQnXQlGqSTJswMzkBuW6QyM5hf35J',
                'object': 'checkout.session',
                'after_expiration': None,
                'allow_promotion_codes': None,
                'amount_subtotal': 3000,
                'amount_total': 3000,
                'automatic_tax': {
                    'enabled': False,
                    'liability': None,
                    'status': None,
                },
                'billing_address_collection': None,
                'cancel_url': 'https://httpbin.org/post',
                'client_reference_id': None,
                'client_secret': None,
                'consent': None,
                'consent_collection': None,
                'created': 1726539734,
                'currency': 'usd',
                'currency_conversion': None,
                'custom_fields': [],
                'custom_text': {
                    'after_submit': None,
                    'shipping_address': None,
                    'submit': None,
                    'terms_of_service_acceptance': None,
                },
                'customer': None,
                'customer_creation': 'if_required',
                'customer_details': {
                    'address': {
                        'city': 'South San Francisco',
                        'country': 'US',
                        'line1': '354 Oyster Point Blvd',
                        'line2': None,
                        'postal_code': '94080',
                        'state': 'CA',
                    },
                    'email': 'stripe@example.com',
                    'name': 'Jenny Rosen',
                    'phone': None,
                    'tax_exempt': 'none',
                    'tax_ids': [],
                },
                'customer_email': None,
                'expires_at': 1726626134,
                'invoice': None,
                'invoice_creation': {
                    'enabled': False,
                    'invoice_data': {
                        'account_tax_ids': None,
                        'custom_fields': None,
                        'description': None,
                        'footer': None,
                        'issuer': None,
                        'metadata': {},
                        'rendering_options': None,
                    },
                },
                'livemode': False,
                'locale': None,
                'metadata': {},
                'mode': 'payment',
                'payment_intent': 'pi_3Pzr3UP4KnHuV8I20uYi6yjl',
                'payment_link': None,
                'payment_method_collection': 'if_required',
                'payment_method_configuration_details': None,
                'payment_method_options': {
                    'card': {'request_three_d_secure': 'automatic'}
                },
                'payment_method_types': ['card'],
                'payment_status': 'paid',
                'phone_number_collection': {'enabled': False},
                'recovered_from': None,
                'saved_payment_method_options': None,
                'setup_intent': None,
                'shipping_address_collection': None,
                'shipping_cost': None,
                'shipping_details': None,
                'shipping_options': [],
                'status': 'complete',
                'submit_type': None,
                'subscription': None,
                'success_url': 'https://httpbin.org/post',
                'total_details': {
                    'amount_discount': 0,
                    'amount_shipping': 0,
                    'amount_tax': 0,
                },
                'ui_mode': 'hosted',
                'url': None,
            },
            'previous_attributes': None,
        },
    }
