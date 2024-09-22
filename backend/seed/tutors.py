from faker import Faker

from backend.schemas.api.tutor_accounts import (
    TutorApplication,
    TutorApplicationDocument,
    TutorInfo,
)
from backend.services.tutors import (
    create_tutor_application,
    update_tutor_info,
)
from tests.utils.file import upload_test_file

faker = Faker()


def get_random_tutor_info():
    return {
        'about_description': faker.text(),
        'years_of_exp': faker.random_int(min=1, max=10),
        'experience_description': faker.text(),
        'native_lang': faker.language_code(),
        'spoken_langs': [
            faker.language_code() for _ in range(faker.random_int(min=1, max=5))
        ],
        'preferred_curriculum': faker.random_elements(
            elements=('British', 'American', 'IB', 'CBSE', 'ICSE'), length=1
        ),
        'preferred_subjects': faker.random_elements(
            elements=(
                'Math',
                'Science',
                'English',
                'History',
                'Geography',
                'Computer Science',
            ),
            length=faker.random_int(min=1, max=4),
        ),
        'preferred_school_levels': faker.random_elements(
            elements=('Primary', 'Middle', 'High'),
            length=faker.random_int(min=1, max=3),
        ),
        'preferred_tutoring_type': faker.random_element(
            elements=('Online', 'In-Person', 'Both')
        ),
        'available_hr_per_week': faker.random_element(
            elements=('10-20', '20-30', '30-40', '40+')
        ),
        'clean_convicted': 'Yes',
        'online_rate': faker.random_int(min=1, max=100),
        'in_person_rate': faker.random_int(min=1, max=100),
    }


def get_random_tutor_application_document(id, document_type='unknown'):
    return {'file_id': id, 'document_type': document_type}


def get_random_tutor_application(document_id: int):
    return {
        'id_files': [
            get_random_tutor_application_document(document_id, 'identity')
            for _ in range(faker.random_int(min=1, max=3))
        ],
        'cv_files': [
            get_random_tutor_application_document(document_id, 'cv')
            for _ in range(faker.random_int(min=1, max=3))
        ],
        'police_clearence': [
            get_random_tutor_application_document(document_id, 'police_clearence')
            for _ in range(faker.random_int(min=1, max=3))
        ],
        'tutor_work_permit': [
            get_random_tutor_application_document(document_id, 'work_permit')
            for _ in range(faker.random_int(min=1, max=3))
        ],
        'proof_of_exp': [
            get_random_tutor_application_document(document_id, 'proof_of_exp')
            for _ in range(faker.random_int(min=1, max=3))
        ],
    }


def get_random_tutor_availability():
    return {
        'daily_availabilities': [
            {
                'day': 'monday',
                'start_time': '08:00',
                'end_time': '10:00',
            },
            {
                'day': 'tuesday',
                'start_time': '08:00',
                'end_time': '10:00',
            },
        ]
    }


def update_tutor_info_record(db, user_id):
    tutor_info = get_random_tutor_info()

    update_tutor_info(db, user_id, TutorInfo(**tutor_info))


def create_tutor_application_record(db, user_id, monkeypatch):
    db_file = upload_test_file('test.pdf', db, monkeypatch)

    payload = get_random_tutor_application(db_file.id)

    payload_schema = TutorApplication(
        cv_files=[TutorApplicationDocument(**item) for item in payload['cv_files']],
        id_files=[TutorApplicationDocument(**item) for item in payload['id_files']],
        police_clearence=[
            TutorApplicationDocument(**item) for item in payload['police_clearence']
        ],
        tutor_work_permit=[
            TutorApplicationDocument(**item) for item in payload['tutor_work_permit']
        ],
        proof_of_exp=[
            TutorApplicationDocument(**item) for item in payload['proof_of_exp']
        ],
    )

    return create_tutor_application(db, user_id, payload_schema)
