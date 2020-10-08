from flask import Flask
import src.Utility
from src.client import chat_bluePrint    

def create_app():
    app = Flask(__name__) 
    if(app.config["ENV"] == "total_development"):
        app.config.from_object("config.FullLocalConfig")
     
    elif (app.config["ENV"] == "core_development"):
        app.config.from_object("config.CoreLocalConfig") 
        
    elif (app.config["ENV"] == "service_development"):
        app.config.from_object("config.ServiceLocalConfig") 
     
    elif (app.config["ENV"] == "client_development"):
        app.config.from_object("config.ClientLocalConfig") 
        
    elif (app.config["ENV"] == "production"):
        app.config.from_object("config.ProdConfig") 

    app.register_blueprint(chat_bluePrint)    
    return app
