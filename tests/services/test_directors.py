from unittest.mock import MagicMock

import pytest

from app.dao.models.director import Director
from app.dao.director import DirectorDAO
from app.services.director import DirectorService


@pytest.fixture
def director_dao():
    director_dao = DirectorDAO(None)
    director1 = Director(id=1, name="dir1")
    director2 = Director(id=2, name="dir2")
    director3 = Director(id=3, name="Great Kojima")

    directors = {1: director1, 2: director2, 3: director3}
    director_dao.get_one = MagicMock(side_effect=directors.get)
    director_dao.get_all = MagicMock(return_value=directors)
    director_dao.create = MagicMock(return_value=Director(id=4))
    director_dao.delete = MagicMock(side_effect=directors.pop)
    director_dao.update = MagicMock()
    director_dao.update_partial = MagicMock()

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0

    def test_create(self):
        director_d = {"name": "Chiko"}
        director = self.director_service.create(director_d)
        assert director.id is not None

    def test_delete(self):
        self.director_service.delete(1)
        director = self.director_service.get_one(1)
        assert director is None

    def test_update(self):
        director_d = {"id": 2, "name": "Pluto"}
        self.director_service.update(director_d)

    def test_update_partial(self):
        director_d = {"id": 3, "name": "just Kojima"}
        self.director_service.update_partial(director_d)
