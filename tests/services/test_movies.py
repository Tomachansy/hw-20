from unittest.mock import MagicMock

import pytest

from app.dao.models.movie import Movie
from app.dao.movie import MovieDAO
from app.services.movie import MovieService


@pytest.fixture
def movie_dao():
    movie_dao = MovieDAO(None)
    movie1 = Movie(
        title="Йеллоустоун",
        description="Владелец ранчо пытается сохранить землю своих предков. Кевин Костнер в неовестерне от автора «Ветреной реки»",
        trailer="https://www.youtube.com/watch?v=UKei_d0cbP4",
        year=2018,
        rating=8.6,
        genre_id=17,
        director_id=1,
        id=1
    )
    movie2 = Movie(
        title="Омерзительная восьмерка",
        description="США после Гражданской войны. Легендарный охотник за головами Джон Рут по кличке Вешатель конвоирует заключенную. По пути к ним прибиваются еще несколько путешественников. Снежная буря вынуждает компанию искать укрытие в лавке на отшибе, где уже расположилось весьма пестрое общество: генерал конфедератов, мексиканец, ковбой… И один из них - не тот, за кого себя выдает.",
        trailer="https://www.youtube.com/watch?v=lmB9VWm0okU",
        year=2015,
        rating=7.8,
        genre_id=4,
        director_id=2,
        id=2
    )
    movie3 = Movie(
        title="Вооружен и очень опасен",
        description="События происходят в конце XIX века на Диком Западе, в Америке. В основе сюжета — сложные перипетии жизни работяги — старателя Габриэля Конроя. Найдя нефть на своем участке, он познает и счастье, и разочарование, и опасность, и отчаяние...",
        trailer="https://www.youtube.com/watch?v=hLA5631F-jo",
        year=1978,
        rating=6,
        genre_id=17,
        director_id=3,
        id=3
    )
    movies = {1: movie1, 2: movie2, 3: movie3}
    movie_dao.get_one = MagicMock(side_effect=movies.get)
    movie_dao.get_all = MagicMock(return_value=movies)
    movie_dao.create = MagicMock(return_value=Movie(id=4))
    movie_dao.delete = MagicMock(side_effect=movies.pop)
    movie_dao.update = MagicMock()
    movie_dao.update_partial = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0

    def test_create(self):
        movie_d = {"title": "test",
                   "description": "test, test, test...",
                   "trailer": "great movie!",
                   "year": 2022,
                   "rating": 10,
                   "genre_id": 7,
                   "director_id": 5}
        movie = self.movie_service.create(movie_d)
        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(1)
        movie = self.movie_service.get_one(1)
        assert movie is None

    def test_update(self):
        movie_d = {"title": "test2",
                   "description": "test1, test2, test3...",
                   "trailer": "great movie, really!",
                   "year": 2023,
                   "rating": 11,
                   "genre_id": 6,
                   "director_id": 3,
                   "id": 2}
        self.movie_service.update(movie_d)

    def test_update_partial(self):
        movie_d = {"trailer": "not really!",
                   "rating": 6,
                   "id": 2}
        self.movie_service.update_partial(movie_d)

