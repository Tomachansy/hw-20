from flask import request
from flask_restx import Resource, Namespace

from app.container import movie_service
from app.dao.models.movie import MovieSchema, Movie

movies_ns = Namespace('movies')


@movies_ns.route('/')
class MoviesView(Resource):

    def get(self):
        movies_schema = MovieSchema(many=True)
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        year = request.args.get('year')

        if director_id and genre_id and year:
            all_movies = Movie.query.filter_by(director_id=director_id, genre_id=genre_id, year=year).all()
        elif director_id and genre_id:
            all_movies = Movie.query.filter_by(director_id=director_id, genre_id=genre_id).all()
        elif director_id and year:
            all_movies = Movie.query.filter_by(director_id=director_id, year=year).all()
        elif genre_id and year:
            all_movies = Movie.query.filter_by(genre_id=genre_id, year=year).all()
        elif director_id:
            all_movies = Movie.query.filter_by(director_id=director_id).all()
        elif genre_id:
            all_movies = Movie.query.filter_by(genre_id=genre_id).all()
        elif year:
            all_movies = Movie.query.filter_by(year=year).all()
        else:
            all_movies = movie_service.get_all()

        if all_movies:
            return movies_schema.dump(all_movies), 200
        else:
            return "", 404

    def post(self):
        req_json = request.json
        new_movie = movie_service.create(req_json)

        return "", 201, f"Location: movie id is {new_movie.id}"


@movies_ns.route('/<int:id>')
class MovieView(Resource):

    def get(self, id):
        movie = movie_service.get_one(id)
        if movie:
            movie_schema = MovieSchema()
            return movie_schema.dump(movie), 200
        else:
            return "", 404

    def put(self, id):
        if id:
            req_json = request.json
            req_json["id"] = id
            movie_service.update(req_json)
            return "", 204
        else:
            return "", 404

    def patch(self, id):
        if id:
            req_json = request.json
            req_json["id"] = id
            movie_service.update_partial(req_json)
            return "", 204
        else:
            return "", 404

    def delete(self, id):
        if id:
            movie_service.delete(id)
            return "", 204
        else:
            return "", 404
