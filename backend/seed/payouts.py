from faker import Faker
from sqlalchemy.orm import Session as Sesssion
from sqlalchemy.sql import func

from backend.models.Payout import Payout
from backend.schemas.models.Payout import PayoutCreate
from backend.services.payouts import create_payout

fake = Faker()
Faker.seed(0)


def generate_random_payout(tutor_id: int) -> dict:
    return {
        'amount': fake.random_int(min=0, max=10000),
        'tutor_id': tutor_id,
    }


def create_payout_record(db, tutor_id):

    payout = generate_random_payout(tutor_id)
    
    payload = PayoutCreate(**payout)

    data = create_payout(db, payout=payload)
    
    return data


def get_list_of_payout_ids(db):
    payouts = db.query(Payout).all()

    return [payout.id for payout in payouts]


def get_random_payout(db: Sesssion):
    return db.query(Payout).order_by(func.random()).first()



