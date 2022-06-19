from flask_restful import Resource
from utils.parsers import tenant_get_args


class TenantView(Resource):
    def get(self):  # Get all tenant callbacks
        args = tenant_get_args.parse_args()
        from app import TenantTable
        company_record = TenantTable.query.filter(
            TenantTable.company_id == args["company_id"]).first()
        return str(company_record), 200

    def post(self):
        return "This resource only supports GET requests.", 405

    def put(self):
        return "This resource only supports GET requests.", 405

    def delete(self):
        return "This resource only supports GET requests.", 405
