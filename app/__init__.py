from flask import Flask

from app.extensions import mongo

from app.webhook.routes import webhook


# Creating our flask app
def create_app():

    app = Flask(__name__)
    
    # mongo.init_app(app)
    app.config['MONGO_URI'] = "mongodb://localhost:27017/webhookdb"
    mongo.init_app(app)
    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
