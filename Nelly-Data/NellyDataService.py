import falcon
from Config import *
from MetaData import *
from bson import json_util
from NellyStore import *
from Utility import *

class ChatServiceRoot(object):
     def on_post(self,req,resp):
        try:
            raw_json = req.bounded_stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)
        try:
            pd = json.loads(raw_json, encoding='utf-8')
            IDList = pd['IDList']
            result = db_getMultipleSessionChat(IDList)
            result = json.dumps(result,default=json_util.default)
            resp.status = falcon.HTTP_200
            resp.body = result
            print("Return data length {0}".format(len(result)))
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid JSON', 'Invalid JSON')

class ChatService(object):
    def on_post(self, req, resp,SessionID):
        try:
            raw_json = req.bounded_stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)
        try:
            pd = json.loads(raw_json, encoding='utf-8')
            Message = pd['Message']
            Response = pd['Response']
            cd = ChatData()
            cd.SessionID = str(SessionID)
            cd.Message = str(Message)
            cd.Response = str(Response)
            cd.Save()
            resp.status = falcon.HTTP_200
            resp.body =str(cd._id)
            print("Saved:::{0}:::{1}".format(SessionID,str(cd._id)))
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid JSON', 'Invalid JSON')

    def on_get(self, req, resp,SessionID):
        result =db_getChatBySession(SessionID)
        resp.status = falcon.HTTP_200
        result = json.dumps(result,default=json_util.default)
        resp.body = result
        print("Return data length {0}".format(len(result)))

class IRESService(object):
    def on_get(self,req,resp,SessionID):
        result =db_getIRESBySession(SessionID)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result,default=json_util.default)

class EmotionService(object):
    def on_get(self,req,resp,SessionID):
        result =db_getEmotionBySession(SessionID)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result,default=json_util.default)

class ChatByID(object):
    def on_get(self,req,resp,id):
        result = ChatData()
        result.loadFromJson(db_getChatByID(id))
        if result.IRES_ID is not None:
            result.IRESData = result.IRESData.MyJson()
        if result.Emotion_ID is not None:
            result.EmotionData = result.EmotionData.MyJson()
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result.MyJson(),default=json_util.default)

class IRESByID(object):
    def on_get(self,req,resp,id):
        result = IRESData()
        result.loadFromJson(db_getIRESByID(id))
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result.MyJson(),default=json_util.default)

class EmotionByID(object):
    def on_get(self,req,resp,id):
        result = IRESData()
        result.loadFromJson(db_getEmotionByID(id))
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result.MyJson(),default=json_util.default)
