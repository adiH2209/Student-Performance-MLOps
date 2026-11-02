"""Shared PostgreSQL connection helper."""
import os
from sqlalchemy import create_engine


def get_engine():
    url = os.getenv("DATABASE_URL", "postgresql+psycopg2://student:studentpass@localhost:5432/student_performance")
    return create_engine(url, pool_pre_ping=True, future=True)
