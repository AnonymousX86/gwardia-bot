# -*- coding: utf-8 -*-
from os import path
from os.path import sep
from typing import Optional

from sqlalchemy import Column, create_engine, Text, Integer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

_BASE_DIR = path.dirname(path.abspath(__file__))
_ENGINE = create_engine(rf'sqlite:///{_BASE_DIR}{2 * sep}..{2 * sep}birthday.db')

_SESSION = sessionmaker()
_SESSION.configure(bind=_ENGINE)
BASE = declarative_base()


class Birthday(BASE):
    __tablename__ = 'birthdays'
    user_id = Column(Text(18), primary_key=True)
    date_day = Column(Integer)
    date_month = Column(Integer)


def get_birthday(user_id: str) -> Optional[Birthday]:
    s = _SESSION()
    try:
        return s.query(Birthday).filter_by(user_id=user_id).one_or_none()
    finally:
        s.close()


def set_birthday(user_id: str, day: int, month: int) -> Optional[Birthday]:
    s = _SESSION()
    try:
        new_bday = Birthday(user_id=user_id, date_day=day, date_month=month)
        s.add(new_bday)
        s.commit()
        return new_bday
    except IntegrityError:
        s.rollback()
        return None
    finally:
        s.close()


def del_birthday(user_id: str):
    s = _SESSION()
    try:
        bday = s.query(Birthday).filter_by(user_id=user_id).one_or_none()
        s.delete(bday)
        s.commit()
        return bool(bday)
    finally:
        s.close()


def _check_birthday() -> bool:
    s = _SESSION()
    try:
        return bool(s.query(Birthday).filter_by(user_id='309270832683679745').one_or_none())
    finally:
        s.close()


def test_database():
    assert _check_birthday()
