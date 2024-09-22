from faker import Faker
from sqlalchemy.orm import Session as Sesssion
from sqlalchemy.sql import func

from backend.models.BankDetail import BankDetail
from backend.schemas.models.BankDetail import BankDetailCreate
from backend.services.bank_details import create_bank_detail

fake = Faker()
Faker.seed(0)


def generate_random_bank_detail() -> dict:
    return {
        'bank_name': fake.company(),
        'branch': fake.city(),
        'account_name': fake.name(),
        'account_number': fake.bban(),
        'iban_no': fake.iban(),
        'swift_code': fake.swift(),
    }


def create_bank_detail_record(db, tutor_id: int):
    bank_detail = generate_random_bank_detail()

    payload = BankDetailCreate(**bank_detail)

    data = create_bank_detail(db, bank_detail=payload, tutor_id=tutor_id)

    return data


def get_list_of_bank_detail_ids(db):
    bank_details = db.query(BankDetail).all()

    print(bank_details)

    return [bank_detail.id for bank_detail in bank_details]


def get_random_bank_detail(db: Sesssion):
    return db.query(BankDetail).order_by(func.random()).first()
