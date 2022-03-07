from unittest.mock import MagicMock

import pytest

from app.dao.models.genre import Genre
from app.dao.genre import GenreDAO
from app.services.genre import GenreService


@pytest.fixture
def genre_dao():
    genre_dao = GenreDAO(None)
    genre1 = Genre(id=1, name="Fanny")
    genre2 = Genre(id=2, name="Life")
    genre3 = Genre(id=3, name="Drama")

    genres = {1: genre1, 2: genre2, 3: genre3}
    genre_dao.get_one = MagicMock(side_effect=genres.get)
    genre_dao.get_all = MagicMock(return_value=genres)
    genre_dao.create = MagicMock(return_value=Genre(id=4))
    genre_dao.delete = MagicMock(side_effect=genres.pop)
    genre_dao.update = MagicMock()
    genre_dao.update_partial = MagicMock()

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre is not None
        assert genre.id is not None

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) > 0

    def test_create(self):
        genre_d = {"name": "Cuteness"}
        genre = self.genre_service.create(genre_d)
        assert genre.id is not None

    def test_delete(self):
        self.genre_service.delete(1)
        genre = self.genre_service.get_one(1)
        assert genre is None

    def test_update(self):
        genre_d = {"id": 2, "name": "Sucks"}
        self.genre_service.update(genre_d)

    def test_update_partial(self):
        genre_d = {"id": 3, "name": "Drama Queen"}
        self.genre_service.update_partial(genre_d)
