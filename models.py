import os
from flask_sqlalchemy import SQLAlchemy


database_path = ''
# if database_path.startswith("postgres://"):
#     database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()


cast = db.Table('cast',
                db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
                db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'))
                )


class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def format(self):
        new_cast = []
        for c in self.Movie:
            new_cast.append({'id': c.id,
                             'title': c.title})
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': new_cast
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.String, nullable=False)
    cast = db.relationship('Actor', secondary=cast,
                           backref="Movie")

    def format(self):
        new_cast = []
        for c in self.cast:
            print(c.id)
            new_cast.append({'id': c.id,
                             'name': c.name})
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': new_cast
        }

    def insert(self, actors):
        db.session.add(self)
        for actor in actors:
            self.cast.append(actor)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
