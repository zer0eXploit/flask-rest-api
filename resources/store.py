from flask_restful import Resource
from models.store import Store_Model


class Store(Resource):
    def get(self, name):
        try:
            store = Store_Model.get_store(name)

            if store:
                return store.res_json()
            else:
                return {'message': 'Store not found'}, 400
        except:
            return {'message': 'Something went wrong on our server.'}, 500

    def post(self, name):
        try:
            store = Store_Model.get_store(name)

            if store:
                return {'message': f'A store with name {name} already exists.'}, 400

            else:
                store = Store_Model(name)
                store.upsert_store()
                return {'message': 'Store created.'}, 201
        except:
            return {'message': 'Something went wrong on our server.'}, 500

    def delete(self, name):
        try:
            store = Store_Model.get_store(name)
            if store:
                store.delete_store()
                return {}, 204
            else:
                return {'message': f'Store {name} is not found'}, 404
        except:
            return {'message': 'Something went wrong on our server.'}, 500


class Stores_List(Resource):
    def get(self):
        try:
            return {'stores': [store.res_json() for store in Store_Model.query.all()]}
        except:
            {'message': 'Something went wrong on our server.'}, 500
