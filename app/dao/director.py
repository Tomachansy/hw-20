from app.dao.models.director import Director


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        entity_list = self.session.query(Director).all()
        return entity_list

    def get_one(self, did):
        entity_list = self.session.query(Director).get(did)
        return entity_list

    def create(self, data):
        director = Director(**data)

        self.session.add(director)
        self.session.commit()

        return director

    def update(self, director):
        self.session.add(director)
        self.session.commit()

        return director

    def delete(self, did):
        director = self.get_one(did)

        self.session.delete(director)
        self.session.commit()
