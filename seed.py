"""Seed file to create tables for database."""

from models import db
from app import app

# Create Tables
with app.app_context():
    db.drop_all()
    db.create_all()