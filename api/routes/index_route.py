from flask_restplus import Resource

def add_index(api):
    @api.route('/')
    class Index(Resource):
        def get(self):
            return {'hello': 'world'}