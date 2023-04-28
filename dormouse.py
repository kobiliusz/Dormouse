import app_config, db, waitress
from flask_restful import Api, Resource, reqparse
from flask import render_template, jsonify

app = app_config.get_app()
api = Api(app)


@app.route("/")
def index():
    return render_template("index.html")


class Rooms(Resource):
    def get(self):
        return jsonify(db.get_rooms()), 200


class Messages(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('nick', type=str)
        self.reqparse.add_argument('content', type=str)

    def post(self, room_id):
        args = self.reqparse.parse_args()
        db.store_message(args['nick'], args['content'], room_id)
        return {'message': 'Message received.'}, 201

    def get(self, room_id):
        return jsonify(db.get_messages_for_room(room_id)), 200


api.add_resource(Rooms, '/api/rooms')
api.add_resource(Messages, '/api/messages/<int:room_id>')
if __name__ == '__main__':
    waitress.serve(app, host='0.0.0.0', port=80)
