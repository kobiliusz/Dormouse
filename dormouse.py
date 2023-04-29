import datetime

import app_config, db, waitress, message_handlers
from flask_restful import Api, Resource, reqparse
from flask import render_template
from sqlalchemy.orm import class_mapper

app = app_config.get_app()
api = Api(app)


def model_to_dict(obj):
    mapper = class_mapper(obj.__class__)
    result = {}
    for column in mapper.columns:
        name = column.key
        value = getattr(obj, name)
        if isinstance(value, datetime.datetime):
            value = value.timestamp()
        result[name] = value
    return result


@app.route("/")
def index():
    return render_template("index.html"), 200


class Rooms(Resource):
    def get(self):
        db.remove_old_messages()
        return [model_to_dict(room) for room in db.get_rooms()], 200


class Messages(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('nick', type=str)
        self.reqparse.add_argument('content', type=str)

    def post(self, room_id):
        args = self.reqparse.parse_args()
        content = args['content']
        for handler in message_handlers.get_list():
            content = handler.handle(content)
        db.store_message(args['nick'], content, room_id)
        return {'message': 'Message received.'}, 201

    def get(self, room_id):
        return [model_to_dict(msg) for msg in db.get_messages_for_room(room_id)], 200


api.add_resource(Rooms, '/api/rooms')
api.add_resource(Messages, '/api/messages/<int:room_id>')
if __name__ == '__main__':
    waitress.serve(app, host='0.0.0.0', port=80)
