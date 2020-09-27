from flask_script import Manager
from src import create_app

app = create_app() 
if __name__ == '__main__':
     if(app.env == "development"):
        app.config.from_object("config.Config")
        app.run(debug=True)    
     elif(app.env == "production"):
        app.config.from_object("config.ProdConfig")
        context = ('client.crt', 'client.key')
        app.run(host='0.0.0.0', port=5000, ssl_context=context)
        