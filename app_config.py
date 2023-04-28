from flask import Flask
import flask_cors

app = Flask(__name__, static_folder="static/dist")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dormouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_cors.CORS(app)


def get_app():
    return app
