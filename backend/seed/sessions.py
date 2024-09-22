from faker import Faker

fake = Faker()
Faker.seed(0)


def generate_random_session(types: list[str], service_id: int) -> dict:
    return {
        'type': fake.random_element(elements=types or ['Trial', 'Order']),
        'time': fake.date_time_this_month(after_now=True).strftime('%Y-%m-%d %H:%M:%S'),
        'service_id': service_id,
    }
