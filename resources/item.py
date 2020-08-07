from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.item import Item_Model

items = []


class Item(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        "price",
        required=True,
        help="This field can't be empty!",
        type=float
    )

    parser.add_argument(
        "store_id",
        required=True,
        help="Every item needs a store_id!",
        type=int
    )

    @jwt_required()
    def get(self, name):
        try:
            row = Item_Model.get_item(name)
            if row:
                item_json = row.res_json()
                item_json["accessed_by"] = current_identity.username
                return item_json
            return {"message": "Item not found."}, 404
        except:
            return {"message": "Something went wrong on our server."}, 500

    def post(self, name):
        post_data = Item.parser.parse_args()

        try:
            if Item_Model.get_item(name):
                return {"message": f"An item with name {name} already exists."}, 400

            item = Item_Model(name, **post_data)
            item.upsert_item()
            return {"message": "Item created."}, 201
        except:
            return {"message": "Something went wrong on our server."}, 500

    def put(self, name):
        put_data = Item.parser.parse_args()

        item = Item_Model.get_item(name)

        if item:
            item.price = put_data["price"]
            item.store_id = put_data["store_id"]
        else:
            item = Item_Model(name, **put_data)

        try:
            item.upsert_item()
            return item.res_json()
        except:
            return {"message": "Something went wrong on our server."}, 500

    def delete(self, name):
        item = Item_Model.get_item(name)
        if item:
            try:
                item.delete_item()
                return {}, 204
            except:
                return {"message": "Something went wrong on our server."}, 500

        return {"message": f"Item name {name} is not found."}, 404


class Items_List(Resource):
    def get(self):
        try:
            items = [result.res_json() for result in Item_Model.query.all()]
            return {"items": items}
        except:
            return {"message": "Something went wrong on our server."}, 500
