from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
    from seduce_api.database.models import Base, Sensor, Position, Assignment, History
    db.drop_all()
    db.create_all()
