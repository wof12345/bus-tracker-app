from faker import Faker

faker = Faker()

Faker.seed(0)


def get_random_order_review(order_id: int) -> dict:
    return {
        'order_id': order_id,
        'rating': faker.random_int(min=1, max=5),
        'comment': faker.text(),
    }
