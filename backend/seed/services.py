from faker import Faker
from sqlalchemy.orm import Session as Sesssion
from sqlalchemy.sql import func

from backend.models.File import File, FileType
from backend.models.Service import Service
from backend.schemas.models.Service import ServiceCreate
from backend.schemas.models.ServiceCategory import ServiceCategoryCreate
from backend.services.services import create_service, create_service_category

fake = Faker()
Faker.seed(0)


def generate_random_category(parent_id: None = None) -> dict:
    return {
        'name': fake.word(),
        'description': fake.text(max_nb_chars=200),
        'parent_id': parent_id,
    }


def generate_random_service(category_id: int, video_id: int) -> dict:
    return {
        'price': fake.random_int(min=0, max=1000),
        'description': fake.text(max_nb_chars=200),
        'title': fake.word(),
        'video_id': video_id,
        'status': fake.random_element(elements=('Draft', 'Published', 'Archived')),
        'duration': fake.random_element(
            elements=('ThirtyMin', 'FortyFiveMin', 'SixtyMin')
        ),
        'medium': fake.random_element(elements=('Online', 'InPerson')),
        'category_id': category_id,
    }


def create_service_category_record(db):
    category = generate_random_category()

    payload = ServiceCategoryCreate(**category)

    data = create_service_category(db, payload)

    return data


def create_service_record(db, category_id, tutor_id):
    db_file = File(
        name=fake.file_name(),
        path=fake.file_path(),
        hash=fake.sha256(),
        size=fake.random_int(min=0, max=1000),
        type=FileType.video,
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    service = generate_random_service(category_id, db_file.id)

    payload = ServiceCreate(**service)

    data = create_service(db, payload, tutor_id)

    return data


def get_list_of_service_ids(db):
    services = db.query(Service).all()

    return [service.id for service in services]


def get_random_service(db: Sesssion):
    return db.query(Service).order_by(func.random()).first()
