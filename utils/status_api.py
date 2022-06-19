from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class Status(Resource):
    def get(self):
        return 200

    def post(self):
        return "This resource only supports GET requests.", 405

    def put(self):
        return "This resource only supports GET requests.", 405

    def delete(self):
        return "This resource only supports GET requests.", 405


api.add_resource(Status, "/")

if __name__ == "__main__":
    app.run(debug=True)
