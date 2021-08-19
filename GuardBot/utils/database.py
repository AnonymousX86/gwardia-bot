# -*- coding: utf-8 -*-
from sqlalchemy import Column, create_engine, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

_ENGINE = create_engine('sqlite:///../birthday.db')
_SESSION = sessionmaker()
_SESSION.configure(bind=_ENGINE)
BASE = declarative_base()


class Birthday(BASE):
    __tablename__ = 'birthdays'
    user_id = Column(Text(18), primary_key=True)
    date_day = Column(Integer)
    date_month = Column(Integer)


def _check_birthday() -> bool:
    s = _SESSION()
    try:
        return bool(s.query(Birthday).filter_by(user_id='309270832683679745').one_or_none())
    finally:
        s.close()


def test_database():
    assert _check_birthday()
