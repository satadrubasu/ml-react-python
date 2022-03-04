from flask import Flask,jsonify
from flask_restful import Api,Resource
from resource.logisticregression import LogRegression

app = Flask(__name__)
app.secret_key = 'externelizeme'

## restful API wrap no routes needed
api = Api(app)

###### ADDING RESOURCES TO API ########
api.add_resource(LogRegression,'/algo/lr/<string:name>')

if __name__ == '__main__':
    app.run(port=5000)
    #app.run(debug=False)