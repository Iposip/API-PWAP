from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy #db
from flask_marshmallow import Marshmallow #ORM
import os


app = Flask(__name__)
dir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(dir, "db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
marshmallow = Marshmallow(app)


# models


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    status = db.Column(db.Boolean)

    def __init__(self, name, description, status):
        self.name = name
        self.description = description
        self.status = status


class TaskSchema(marshmallow.Schema):
    class Meta:
        fields = (
            "id",
            "name",
            "description",
            "status",
        )


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, name, password):
        self.name = name
        self.password = password


class UserSchema(marshmallow.Schema):
    class Meta:
        fields = (
            "id",
            "name",
            "password",
        )


user_schema = UserSchema()
users_schema = UserSchema(many=True)

# helper


def auth(password):
    userpass = db.session.query(User.password).filter_by(password=password).scalar()
    if password != userpass:
        return False
    return True


# routes


@app.route("/task", methods=["GET"])
def get_tasks():
    all_tasks = Task.query.all()
    return tasks_schema.jsonify(all_tasks)


@app.route("/task/<id>", methods=["GET"])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)


@app.route("/task", methods=["POST"])
def add_task():
    if auth(request.json["password"]) == False:
        return jsonify("Couldn't authenticate user.")

    name = request.json["name"]
    description = request.json["description"]
    status = 0

    exists = db.session.query(Task.name).filter_by(name=name).scalar() is not None
    if not exists:
        new_task = Task(name, description, status)

        db.session.add(new_task)
        db.session.commit()

        return task_schema.jsonify(new_task)
    return jsonify(f"Task with name '{name}' already exists!")


@app.route("/task/<id>", methods=["PUT"])
def update_product(id):
    if auth(request.json["password"]) == False:
        return jsonify("Couldn't authenticate user.")
    task = Task.query.get(id)

    if request.json["name"]:
        task.name = request.json["name"]
    if request.json["description"]:
        task.description = request.json["description"]
    task.status = not task.status

    db.session.commit()

    return task_schema.jsonify(task)


@app.route("/task/<id>", methods=["DELETE"])
def delete_task(id):
    if auth(request.json["password"]) == False:
        return jsonify("Couldn't authenticate user.")

    task = Task.query.get(id)
    if not task:
        return jsonify(f"Task id={id} doesn't exist")
    db.session.delete(task)
    db.session.commit()

    return jsonify(f"Task id={id} deleted")


@app.route("/user", methods=["GET"])
def get_users():
    all_users = User.query.all()
    return users_schema.jsonify(all_users)


# server


if __name__ == "__main__":
    db.create_all()

    name = "ApiUser"
    password = "Api123"

    exists = db.session.query(User.name).filter_by(name=name).scalar() is not None
    if not exists:
        new_user = User(name, password)

        db.session.add(new_user)
        db.session.commit()

    app.run()
