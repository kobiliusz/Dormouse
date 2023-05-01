from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import app_config, rooms

app = app_config.get_app()
db = SQLAlchemy(app)


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    room = db.relationship('Room', backref=db.backref('messages', lazy=True))


def get_rooms():
    return db.session.query(Room).all()


def get_messages_for_room(id_room):
    return db.session.query(Message).filter_by(room_id=id_room).all()


def store_message(nick, content, room_id):
    db.session.add(Message(nick=nick, content=content, room_id=room_id))
    db.session.commit()


def remove_old_messages():
    with app.app_context():
        db.session.query(Message)\
            .filter(Message.time <= datetime.now() - timedelta(days=1)).delete()
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        for room_name in rooms.room_list:
            db.session.add(Room(name=room_name))
        db.session.commit()
