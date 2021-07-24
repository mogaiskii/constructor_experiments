from functools import lru_cache

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app_config import Config
from models import Base


@lru_cache
def get_sessionmaker():
    db_conf = Config.db_url
    engine = create_engine(db_conf, pool_pre_ping=True, echo=True)
    engine.execute('DROP SCHEMA IF EXISTS public CASCADE;')
    engine.execute('CREATE SCHEMA public;')
    engine.execute('CREATE EXTENSION IF NOT EXISTS postgis;')
    meta = Base.metadata
    meta.bind = engine
    meta.create_all()
    return sessionmaker(bind=engine)


@pytest.yield_fixture
def session() -> Session:
    db = get_sessionmaker()
    s = db()
    yield s
    s.close()
