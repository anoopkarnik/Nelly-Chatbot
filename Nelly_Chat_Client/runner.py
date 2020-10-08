from flask_script import Manager
from src import create_app

app = create_app() 
if __name__ == '__main__':
    if(app.env == "total_development"):
        app.config.from_object("config.FullLocalConfig")
        app.run(debug=True) 
        
    elif(app.env == "core_development"):
        app.config.from_object("config.CoreLocalConfig")
        context = ('client.crt', 'client.key')
        app.run(host='0.0.0.0', port=5000, ssl_context=context)  
        
    elif(app.env == "service_development"):
        app.config.from_object("config.ServiceLocalConfig")
        context = ('client.crt', 'client.key')
        app.run(host='0.0.0.0', port=5000, ssl_context=context)
             
    elif(app.env == "client_development"):
        app.config.from_object("config.ClientLocalConfig")
        app.run(debug=True)   
     
    elif(app.env == "production"):
        app.config.from_object("config.ProdConfig")
        context = ('client.crt', 'client.key')
        app.run(host='0.0.0.0', port=5000, ssl_context=context)
        