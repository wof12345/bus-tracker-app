from faker import Faker

from backend.models.OrderResolution import OrderResolution
from backend.schemas.api.order_resolutions import CreateOrderResolutionPayload
from backend.services.order_resolutions import create_order_resolution
from backend.services.session import list_sessions

faker = Faker()

Faker.seed(0)

def get_random_order_resolution(
    order_id: int, types: list[str] = None, session_ids: list[int] = None
) -> dict:
    return {
        'type': faker.random_element(
            elements=(types or ['FullRefund', 'PartialRefund', 'Reschedule'])
        ),
        'description': faker.text(),
        'order_id': order_id,
        'refund_session_ids': session_ids,
        'rescheduled_appointment_slots': [
            {
                'start_time': faker.date_time_this_year(after_now=True).isoformat(),
                'session_id': id,
            }
            for id in session_ids
        ],
    }


def create_order_resolution_record(
    db_session, order_id: int, types: list[str] = None, user_id: int = None
) -> OrderResolution:

    sessions = list_sessions(db_session, order_id)

    session_ids = [session.id for session in sessions]

    resolution_types = types or ['FullRefund', 'PartialRefund', 'Reschedule']

    payload_dict = get_random_order_resolution(order_id, resolution_types, session_ids)
    payload = CreateOrderResolutionPayload(**payload_dict)

    response = create_order_resolution(db_session, payload, user_id)

    return response
