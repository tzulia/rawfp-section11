import datetime
import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import User, UserList, UserLogin

app = Flask(__name__)
app.secret_key = '28dd16028dd1602e2b7b92b2b7b92b79e7e40189df5f30e7e40189df5f30'

# Settings JWT Token to expire after 15 minutes.
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=900)

# Turn off the Flask-SQLAlchemy modification tracker.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Allow the Flask app to see errors from other modules.
app.config['PROPAGATE_EXCEPTIONS'] = True

# Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///things.db')

api = Api(app)
jwt = JWTManager(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(UserLogin, '/auth/login')
api.add_resource(UserRegister, '/auth/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserList, '/users')

# Create DB tables, if they do not exists.
@app.before_first_request
def create_db_tables():
    db.create_all()


if __name__ == '__main__':              # To make sure, not to run this code again on import.
    from db import db
    db.init_app(app)
    app.run(port=5000)
