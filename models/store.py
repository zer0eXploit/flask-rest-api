from db import db


class Store_Model(db.Model):

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('Item_Model', lazy='dynamic')

    # why lazy = dynamic?
    # whenever querying a store, the items with the store_id are created from the Items_Model
    # which is too costly if there are many items
    # as a trade-off, when returning items, self.items.all(), a query, must be made

    def __init__(self, name):
        self.name = name

    def res_json(self):
        return {"name": self.name, "items": [item.res_json() for item in self.items.all()]}

    @classmethod
    def get_store(cls, name):
        return cls.query.filter_by(name=name).first()

    def upsert_store(self):
        # does both insert and update

        db.session.add(self)
        db.session.commit()

    def delete_store(self):
        db.session.delete(self)
        db.session.commit()
