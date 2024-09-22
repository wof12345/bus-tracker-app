from sqlalchemy.orm import Session

from backend.models.Payment import Payment
from backend.utils.stripe_config import get_stripe_client
from seed.orders import get_order_record


def create_payment_record(
    db: Session, order_id: int = None, add_intent_id: bool = False
):
    order = get_order_record(db, order_id)

    payment: Payment = order.payment

    if add_intent_id:
        stripe = get_stripe_client()

        session = stripe.checkout.Session.retrieve(payment.session_id)

        pm = stripe.PaymentMethod.create(
            type='card',
            card={
                'number': '4242424242424242',
                'exp_month': 12,
                'exp_year': 2025,
                'cvc': '123',
            },
        )

        intent = stripe.PaymentIntent.create(
            amount=order.price * 100,
            currency='usd',
            customer=session.customer,
            payment_method=pm.id,
            capture_method='manual',
            automatic_payment_methods={
                'enabled': True,
                'allow_redirects': 'never',
            },
        )

        payment.intent_id = intent.id
        db.commit()

    db.commit()
    db.refresh(payment)

    return payment
