from flask import Flask
import src.Utility
from src.client import chat_bluePrint    

def create_app():
    app = Flask(__name__) 
    if(app.config["ENV"] == "development"):
        app.config.from_object("config.Config")
        
    elif (app.config["ENV"] == "production"):
        app.config.from_object("config.ProdConfig") 

    app.register_blueprint(chat_bluePrint)    
    return app
