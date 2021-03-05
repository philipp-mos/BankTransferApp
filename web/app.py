from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.MoneyManagementDB

users = db["Users"]


def UserExist(username):
    if users.find({"Username": username}).count() == 0:
        return False

    else:
        return True


class Home(Resource):
    def get(self):

        returnJson = {
            "status": 200,
            "message": "Hello world"
        }

        return jsonify(returnJson)


class Register(Resource):
    def post(self):
        
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]


        if UserExist(username):
            returnJson = {
                'status': 301,
                'message': 'Invalid Username'
            }

            return jsonify(returnJson)


        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


        users.insert({
            "Username": username,
            "Password": hashed_password,
            "Own": 0,
            "Debt": 0
        })

        returnJson = {
            "status": 200,
            "message": "You successfully signed up for the API"
        }

        return jsonify(returnJson)




api.add_resource(Home, '/home')
api.add_resource(Register, '/register')




if __name__ == "__main__":
    app.run(host='0.0.0.0')
