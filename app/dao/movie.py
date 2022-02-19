from app.dao.models.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        entity_list = self.session.query(Movie).all()
        return entity_list

    def get_one(self, mid):
        entity_list = self.session.query(Movie).get(mid)
        return entity_list

    def create(self, data):
        movie = Movie(**data)

        self.session.add(movie)
        self.session.commit()

        return movie

    def update(self, movie):
        self.session.add(movie)
        self.session.commit()

        return movie

    def delete(self, mid):
        movie = self.get_one(mid)

        self.session.delete(movie)
        self.session.commit()
