import os
from sqlalchemy import Column, String, Integer, ForeignKey  
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
'''


def db_drop_all():
    db.drop_all()
    db.create_all()

# ROUTES

# New Court model
class Court(db.Model):
    __tablename__ = 'courts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    court_no = Column(Integer, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    max_players = Column(Integer, nullable=False)
    level = Column(String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'court_no': self.court_no,
            'date': self.date,
            'time': self.time,
            'max_players': self.max_players,
            'level': self.level
        })


# New CourtRegistration model
class CourtRegistration(db.Model):
    __tablename__ = 'court_registrations'

    id = Column(Integer, primary_key=True)
    court_id = Column(Integer, ForeignKey('courts.id'), nullable=False)
    name = Column(String, nullable=False)
    player_unique_id = Column(String, nullable=False)
    role = Column(String, nullable=False)
    reg_date_time = Column(String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'court_id': self.court_id,
            'name': self.name,
            'player_unique_id': self.player_unique_id,
            'role': self.role,
            'reg_date_time': self.reg_date_time
        })