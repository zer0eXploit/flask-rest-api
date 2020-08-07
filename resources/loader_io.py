from flask import send_file
from flask_restful import Resource


class Loader(Resource):
    def get(self):
        response = send_file('loaderio-a3d59da2c9ad87df554a0d56197a20e5.txt')

        return response
