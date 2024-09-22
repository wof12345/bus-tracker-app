from faker import Faker

from backend.models.Order import Order
from backend.models.Service import Service
from backend.schemas.api.orders import AppointmentSlot, OrderCreatePayload
from backend.services.order import create_order

faker = Faker()

Faker.seed(0)


def generate_random_order(service_ids):
    return {
        'service_id': faker.random_element(elements=service_ids),
        'appointment_slots': [
            {
                'start_time': str(
                    faker.date_time_this_year(after_now=True).strftime(
                        '%Y-%m-%d %H:%M:%S'
                    )
                )
            }
            for _ in range(faker.random_int(min=6, max=12))
        ],
    }


def create_order_record(db, student_id, tutor_id, service_ids):
    order = generate_random_order(service_ids)

    order['student_id'] = student_id

    payload = OrderCreatePayload(
        service_id=order['service_id'],
        student_id=order['student_id'],
        appointment_slots=[
            AppointmentSlot(start_time=slot['start_time'])
            for slot in order['appointment_slots']
        ],
    )

    service = db.query(Service).filter(Service.id == order['service_id']).first()

    data = create_order(db, payload, student_id, service=service)

    return data


def complete_order(db, order_id):
    order = db.query(Order).filter(Order.id == order_id).first()

    order.status = 'Completed'

    db.commit()

    return order


def get_list_of_order_ids(db):
    return [order.id for order in db.query(Order).all()]


def get_order_record(db, order_id: int = None):
    order = db.query(Order)

    if order_id:
        order = order.filter(Order.id == order_id)

    return order.first()
