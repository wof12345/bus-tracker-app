from faker import Faker

from seed.services import get_random_service

fake = Faker()
Faker.seed(0)


def get_random_trial_session_payload(session):
    service = get_random_service(session)

    return {
        'time': fake.date_time_this_month(after_now=True).strftime('%Y-%m-%d %H:%M:%S'),
        'service_id': service.id,
    }
