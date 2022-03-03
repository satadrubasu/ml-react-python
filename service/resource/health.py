from flask_restful import Resource

class Health(Resource):
    def get(self):
        return {'message':'App is Alive!'}
