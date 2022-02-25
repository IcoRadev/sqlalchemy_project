from flask import Flask, request

from allocation.adapters import orm
from allocation.domain import batch_entity
from allocation.domain.model import chat_session_entity
from allocation.config import get_configuration as cfg
from allocation.service_layer import services, unit_of_work

# Start flask
app = Flask(__name__)
# Set DB uri
app.config['SECRET_KEY'] = cfg()["API_KEY"]
orm.start_mappers()


@app.route("/batch", methods=["GET", "POST", "DELETE"])
def add_batch():
    if request.method == "POST":
        try:
            batch_item = batch_entity.Batch("ChatSession", request.json["tag"])
            services.add_batch(unit_of_work.SqlAlchemyUnitOfWork(),
                               batch_item)

            return "OK", 201

        except Exception as message:
            return str(message), 500


@app.route("/chat_session", methods=["POST", "GET", "DELETE"])
def chat_session():
    if request.method == "POST":
        try:
            chat_entity = chat_session_entity.ChatSession(
                request.json["representative_id"],
                request.json["user_id"],
                request.json["website_session_id"],
                request.json["start_time"],
                request.json["end_time"],
            )
            services.add_batch(
                            unit_of_work.SqlAlchemyUnitOfWork(), chat_entity)

        except Exception as message:
            return str(message), 500

        return "OK", 201

    elif request.method == "GET":
        try:
            entity_id = request.json["id"]
            entity = services.get_batch(unit_of_work.SqlAlchemyUnitOfWork(),
                                        chat_session_entity.ChatSession,
                                        int(entity_id))

        except Exception as message:
            return str(message), 500

        return str(entity), 200

    elif request.method == "DELETE":
        try:
            entity_id = request.json["id"]
            services.remove_batch(unit_of_work.SqlAlchemyUnitOfWork(),
                                  chat_session_entity.ChatSession,
                                  int(entity_id))

        except Exception as message:
            return str(message), 500

        return "OK", 200


@app.route("/batch", methods=["GET", "POST", "DELETE"])
def batch():
    if request.method == "POST":
        try:
            chat_entity = chat_session_entity.ChatSession(
                request.json["representative_id"],
                request.json["user_id"],
                request.json["website_session_id"],
                request.json["start_time"],
                request.json["end_time"],
            )
            services.add_entity(
                unit_of_work.SqlAlchemyUnitOfWork(), chat_entity)

        except Exception as message:
            return str(message), 500

        return "OK", 201
