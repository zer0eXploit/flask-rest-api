import os
from flask_jwt import JWT
from flask_restful import Resource, Api
from flask import Flask
from datetime import timedelta
from security import authenticate, identity
from resources.user import User_Register
from resources.item import Item, Items_List
from resources.store import Store, Stores_List
from resources.home import Home
from resources.loader_io import Loader


app = Flask(__name__)
app.secret_key = "this_is_something_secret_that_you_should_nt_share"

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db'
)
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['JWT_NOT_BEFORE_DELTA'] = timedelta(seconds=120)

api = Api(app)

jwt = JWT(app, authenticate, identity)  # creates /auth

api.add_resource(Home, "/")
api.add_resource(Loader, "/loaderio-a3d59da2c9ad87df554a0d56197a20e5")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(Stores_List, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items_List, "/items")
api.add_resource(User_Register, "/register")


if __name__ == "__main__":
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
