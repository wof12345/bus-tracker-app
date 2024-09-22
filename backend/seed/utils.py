import faker
faker = faker.Faker()

def get_file(types):
    return {
        "name": faker.file_name(),
        "type": faker.random_choices(elements=types or ["image", "video", "document"], length=1)[0],
        "size": faker.random_int(min=1000, max=100000),
        "path": "studybuddies/416085322_387435977103897_2859654536312535126_n.jpg",
        "hash": faker.sha256(),
    }