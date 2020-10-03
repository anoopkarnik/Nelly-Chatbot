import falcon
import json
from NellyDataService import *
from Config import *
from wsgiref.simple_server import make_server
from falcon_swagger_ui import register_swaggerui_app
import pathlib


cls = falcon.API()
cls.req_options.auto_parse_form_urlencoded=True

_chatService = ChatService()
cls.add_route('/{SessionID}', _chatService)
cls.add_route('/Chat/{SessionID}', _chatService)

_iresService = IRESService()
cls.add_route('/IRES/{SessionID}', _iresService)

_emotionService = EmotionService()
cls.add_route('/Emotion/{SessionID}', _emotionService)

_chatByIDService = ChatByID()
cls.add_route('/ChatByID/{id}',_chatByIDService)

_IRESByIDService = IRESByID()
cls.add_route('/IRESByID/{id}',_IRESByIDService)

_EmotionByIDService = EmotionByID()
cls.add_route('/EmotionByID/{id}',_EmotionByIDService)


SCHEMA_URL = '/static/swagger.json'
STATIC_PATH = '/home/ubuntu/Nelly8001/Nelly-Data/static'
cls.add_static_route('/static', str(STATIC_PATH))
register_swaggerui_app(
    cls, '/swagger', SCHEMA_URL,
    page_title='Swagger:Nelly Data Service',
    favicon_url='https://falconframework.org/favicon-32x32.png',
    config={'supportedSubmitMethods': ['get'], }
)

#waitress-serve --port=8000 things:app

if __name__ == '__main__':
    _port =int(Config.Http_Config['Port'])
    print('Please connect to the link: http://{}:{}/'.format('', _port))
    httpd = make_server('0.0.0.0',_port, cls)
    httpd.serve_forever()