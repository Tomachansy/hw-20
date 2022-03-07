from flask import request
from flask_restx import Resource, Namespace

from app.implemented import movie_service
from app.dao.models.movie import MovieSchema, Movie
from app.helpers.decorators import auth_required, admin_required

movies_ns = Namespace('movies')


@movies_ns.route('/')
class MoviesView(Resource):
    @auth_required
    def get(self):
        all_movies = Movie.query.filter_by(**request.args).all()

        if all_movies:
            res = MovieSchema(many=True).dump(all_movies)
            return res, 200
        else:
            return "", 404

    @admin_required
    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)

        return "", 201, {"location": f"/movies/{movie.id}"}


@movies_ns.route('/<int:id>')
class MovieView(Resource):
    @auth_required
    def get(self, id):
        movie = movie_service.get_one(id)
        if movie:
            movie_schema = MovieSchema()
            return movie_schema.dump(movie), 200
        else:
            return "", 404

    @admin_required
    def put(self, id):
        if id:
            req_json = request.json
            req_json["id"] = id
            movie_service.update(req_json)
            return "", 204
        else:
            return "", 404

    @admin_required
    def patch(self, id):
        if id:
            req_json = request.json
            req_json["id"] = id
            movie_service.update_partial(req_json)
            return "", 204
        else:
            return "", 404

    @admin_required
    def delete(self, id):
        if id:
            movie_service.delete(id)
            return "", 204
        else:
            return "", 404
