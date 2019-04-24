from datetime import datetime
from flask import Flask, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
database = os.environ['POSTGRES_DATABASE']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@postgres/{}'.format(user, password, database)
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    dob = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, dob):
        self.username = username
        self.dob = dob

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'dob')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    username = request.json['username']
    dob = request.json['dob']
    new_user = User(username, dob)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user)

# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)

# endpoint to get user detail by username
@app.route("/user/<username>", methods=["GET"])
def user_detail(username):
    user = User.query.get(username)
    user_data = user_schema.jsonify(user)
    dob = datetime.strptime(json.loads(user_data.response[0]) \
        ["dob"], '%Y-%m-%dT%H:%M:%S%z').date()
    dob = dob.replace(year=datetime.today().year)
    today = datetime.now().date()
    delta =  (dob - today).days
    delta = abs(delta)
    
    if delta == 0:
        return jsonfiy(message = "Hello {}! Happy \
            birthday!".format(username))

    return jsonify(message = "Hello {}! Your birthday \
        is in {} days".format(username, delta))

  
# endpoint to update user
@app.route("/user/<username>", methods=["PUT"])
def user_update(username):
    user = User.query.get(username)
    username = request.json['username']
    dob = request.json['dob']
    user.dob = dob
    user.username = username
    db.session.commit()
    return user_schema.jsonify(user)


# endpoint to delete user
@app.route("/user/<username>", methods=["DELETE"])
def user_delete(username):
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)