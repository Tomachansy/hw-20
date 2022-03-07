from flask import request
from flask_restx import Resource, Namespace

from app.implemented import director_service
from app.dao.models.director import DirectorSchema
from app.helpers.decorators import auth_required, admin_required

directors_ns = Namespace('directors')


@directors_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        all_directors = director_service.get_all()
        if all_directors:
            directors_schema = DirectorSchema(many=True)
            return directors_schema.dump(all_directors), 200
        else:
            return "", 404

    @admin_required
    def post(self):
        req_json = request.json
        director = director_service.create(req_json)

        return "", 201, {"location": f"/directors/{director.id}"}


@directors_ns.route('/<int:id>')
class DirectorView(Resource):
    @auth_required
    def get(self, id):
        director = director_service.get_one(id)
        if director:
            director_schema = DirectorSchema()
            return director_schema.dump(director), 200
        else:
            return "", 404

    @admin_required
    def put(self, id):
        if id:
            req_json = request.json
            req_json["id"] = id
            director_service.update(req_json)
            return "", 204
        else:
            return "", 404

    @admin_required
    def patch(self, id):
        if id:
            req_json = request.json
            req_json["id"] = id
            director_service.update_partial(req_json)
            return "", 204
        else:
            return "", 404

    @admin_required
    def delete(self, id):
        if id:
            director_service.delete(id)
            return "", 204
        else:
            return "", 404
