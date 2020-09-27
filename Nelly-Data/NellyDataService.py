import falcon
from Config import *
from MetaData import *
from bson import json_util

class NellyDataService(object):

    def on_post(self, req, resp,SessionID):
        try:
            raw_json = req.bounded_stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)
        try:
            pd = json.loads(raw_json, encoding='utf-8')
            Message = pd['Message']
            Response = pd['Response']
            cd = ChatData(SessionID)
            cd.Message = str(Message)
            cd.Response = str(Response)
            cd.ModelType = Config.Version['ModelType']
            cd.ModelVersion = Config.Version['ModelVersion']
            thrSave = threading.Thread(target=cd.Save)
            thrSave.start()
            resp.status = falcon.HTTP_200
            resp.body = cd.Message
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid JSON', 'Invalid JSON')

    def on_get(self, req, resp,SessionID):
        cd = ChatData(SessionID)
        result =cd.GetChat()
        chatlist = [chat for chat in result]
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(chatlist,default=json_util.default)