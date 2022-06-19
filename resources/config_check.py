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
        if "FLEET_MANAGEMENT_URI" in os.environ:
            output.update({"Fleet URL": os.environ["FLEET_MANAGEMENT_URI"]})
        else:
            output.update({"Fleet URL": "None parsed."})
        if "FLEET_AUTH_TOKEN" in os.environ:
            output.update({"Fleet Token": os.environ["FLEET_AUTH_TOKEN"]})
        else:
            output.update({"Fleet Token": "None parsed."})

        return output, 200

    def post(self):
        return "This resource only supports GET requests.", 405

    def put(self):
        return "This resource only supports GET requests.", 405

    def delete(self):
        return "This resource only supports GET requests.", 405
