import falcon
import json
from NellyDataService import *
from Config import *
from wsgiref.simple_server import make_server

cls = falcon.API()
cls.req_options.auto_parse_form_urlencoded=True
service = NellyDataService()
cls.add_route('/{SessionID}', service)

#waitress-serve --port=8000 things:app

if __name__ == '__main__':
    _port =int(Config.Http_Config['Port'])
    print('Please connect to the link: http://{}:{}/'.format('', _port))
    httpd = make_server('0.0.0.0',_port, cls)
    httpd.serve_forever()