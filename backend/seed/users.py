from faker import Faker

from backend.models.User import User
from backend.schemas.models.User import UserCreate
from backend.services.auth import create_access_token
from backend.services.user import create_user

faker = Faker()
Faker.seed(0)


def get_random_user(roles):
    return {
        'first_name': faker.first_name_male(),
        'last_name': faker.last_name_male(),
        'email': faker.email(),
        'password': '12345678',
        'role': faker.random_choices(elements=roles or ['tutor', 'student'], length=1)[
            0
        ],
    }


def get_random_user_address():
    return {
        'street_address': faker.street_address(),
        'city': faker.city(),
        'country': faker.country(),
    }


def get_random_user_info():
    return {
        'phone': '+8801712345678',
        'gender': faker.random_element(elements=('M', 'F')),
        'date_of_birth': faker.date_of_birth().isoformat(),
        'nationality': faker.country(),
        'address': get_random_user_address(),
    }


def create_user_record(session, user_roles):
    user = get_random_user(user_roles)

    data = create_user(
        session,
        UserCreate(
            first_name=user['first_name'],
            last_name=user['last_name'],
            email=user['email'],
            password=user['password'],
            role=user['role'],
        ),
    )

    return data


def get_tutor_access_token(db, user_id=None):
    db_user = db.query(User)

    if user_id:
        db_user = db_user.filter(User.id == user_id)

    db_user = db_user.filter(User.role == 'tutor').first()

    token = create_access_token(db, db_user.id)

    return token


def get_tutor_record(db):
    db_user = db.query(User).filter(User.role == 'tutor').first()

    return db_user.tutor


def get_student_access_token(db, user_id=None):
    db_user = db.query(User)

    if user_id:
        db_user = db_user.filter(User.id == user_id)

    db_user = db_user.filter(User.role == 'student').first()

    token = create_access_token(db, db_user.id)

    return token


def get_student_record(db):
    db_user = db.query(User).filter(User.role == 'student').first()

    return db_user.student


def get_admin_access_token(db, user_id=None):
    db_user = db.query(User)

    if user_id:
        db_user = db_user.filter(User.id == user_id)

    db_user = db_user.filter(User.role == 'admin').first()

    token = create_access_token(db, db_user.id)

    return token
