from flask_restful import Resource


class ConfigCheck(Resource):
    def get(self):
        import os
        from app import app
        output = {
            "Database URI": app.config["SQLALCHEMY_DATABASE_URI"],
            "SQLAlchemy Tracking": app.config["SQLALCHEMY_TRACK_MODIFICATIONS"],
            "Time Buffer": os.environ["TIME_BUFFER_MINUTES"],
        }
        if "VERBOSE" in app.config:
            output.update({"Verbose": app.config["VERBOSE"]})
        if "WEBSITE_HOSTNAME" in os.environ:
            output.update({"Hostname": os.environ["WEBSITE_HOSTNAME"]})
        return output, 200

    def post(self):
        return "This resource only supports GET requests.", 405

    def put(self):
        return "This resource only supports GET requests.", 405

    def delete(self):
        return "This resource only supports GET requests.", 405
