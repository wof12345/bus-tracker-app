from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from backend.models.Message import ChatRoom, ChatRoomParticipant, Message
from backend.schemas.models.Message import ChatRoom as ChatRoomSchema
from backend.schemas.models.Message import ChatRoomCreate, MessageCreate
from backend.schemas.models.Message import Message as MessageSchema
from backend.services.chatroom import (
    can_access_chatroom,
    count_chatrooms,
    count_messages,
    create_chatroom,
    create_message,
    get_chatroom,
    list_chatrooms,
    list_messages,
)
from seed.users import get_student_record, get_tutor_record

faker = Faker()
Faker.seed(0)


def get_random_chatroom_payload(db: Session) -> dict:
    tutor = get_tutor_record(db)

    return {
        'name': faker.sentence(),
        'participants': [tutor.user.id],
    }


def create_chatroom_record(db: Session) -> ChatRoomSchema:
    student = get_student_record(db)

    payload = get_random_chatroom_payload(db)
    return create_chatroom(db, ChatRoomCreate(**payload), student.user.id)


def clear_chatroom_records(db: Session) -> None:
    db.query(Message).delete()
    db.query(ChatRoomParticipant).delete()
    db.query(ChatRoom).delete()
    db.commit()


def get_random_message_payload(db: Session, room_id: int) -> dict:
    return {
        'content': faker.sentence(),
        'room_id': room_id,
    }


def create_message_record(db: Session, room_id: int, user_id) -> MessageSchema:
    payload = get_random_message_payload(db, room_id)
    return create_message(db, MessageCreate(**payload), user_id)
