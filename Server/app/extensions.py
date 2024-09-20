from flask_pymongo import PyMongo
#flask mongo connection

mongo = PyMongo()
def init_mongo(app):
    mongo.init_app(app)
    return mongo