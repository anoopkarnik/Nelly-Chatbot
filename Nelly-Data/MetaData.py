# Chat Meta Data Structure
import json
from Utility import *
from NellyStore import *
from datetime import datetime
from Config import *
from json import JSONEncoder

class ChatData(object):
    def __init__(self):
        self.SessionID = None
        self.Message = None
        self.Response = None
        self.TimeStamp = str(datetime.utcnow())
        self.IRESData = None
        self.EmotionData = None 
        self.Emotion_ID = None
        self.IRES_ID = None
    def load(self):
        _threads = []
        _threads.append(threading.Thread(name='OpenIE', target=self.__loadIRES))
        _threads.append(threading.Thread(name='Emotion', target=self.__loadEmotion))
        for _th in _threads:
            _th.start()
        for _th in _threads:
            _th.join()
        _threads.clear()

    def MyJson(self):
        return GetJson(self)

    def Save(self):
        self.__SaveThis()
        _thread = threading.Thread(name='SaveOtherID', target=self.__UpdateOtherID)
        _thread.start()
        return self._id
   
    def __SaveThis(self):
        _db = get_data_coll()
        _t_EmotionData = self.EmotionData
        _t_IRESData = self.IRESData
        self.EmotionData = None
        self.IRESData = None
        if '_id' in dir(self):
            inserted_id = UpdateOne(_db,self)
        else:
            inserted_id = InsertOne(_db,self)
            self._id=inserted_id
        self.EmotionData = _t_EmotionData
        self.IRESData = _t_IRESData

    def __UpdateOtherID(self):
        self.load()
        _threads = []
        _threads.append(threading.Thread(name='OpenIE', target=self.IRESData.Save))
        _threads.append(threading.Thread(name='Emotion', target=self.EmotionData.Save))
        for _th in _threads:
            _th.start()
        for _th in _threads:
            _th.join()
        _threads.clear()
        self.Emotion_ID = str(self.EmotionData.__dict__.get('_id'))
        self.IRES_ID =  str(self.IRESData.__dict__.get('_id'))
        self.__SaveThis()
    
    def __loadEmotion(self):
        if self.EmotionData is None:
            self.EmotionData = EmotionData()
            self.EmotionData.SessionID =self.SessionID
            self.EmotionData.Message = self.Message
            self.EmotionData.load()
    def __loadIRES(self):
        if self.IRESData is None:
            self.IRESData = IRESData()
            self.IRESData.SessionID =self.SessionID
            self.IRESData.Message = self.Message
            self.IRESData.load()
    def loadFromJson(self,dbjsondata):
        for (k, v) in dbjsondata.items():
                setattr(self,k,v)
        if self.Emotion_ID is not None:
            self.EmotionData = EmotionData()
            self.EmotionData.loadFromJson(db_getEmotionByID(self.Emotion_ID))
        if self.IRES_ID is not None:
            self.IRESData = IRESData()
            self.IRESData.loadFromJson(db_getIRESByID(self.IRES_ID))

class IRESData:
    def __init__(self):
        self.Message = None
        self.SessionID = None
        self.Version = None
        self.Type = None
        self.Data = None        
    def load(self):
        if self.Version is None:
            self.Version = str(Config.Version['IRESVersion'])
        if self.Type is None:
            self.Type = str(Config.Version['IRESType'])
        if self.Data is None:
            if self.Message is not None and self.SessionID is not None:
                self.Data = InvokeOpenIE(self.Message)
    def MyJson(self):
        return GetJson(self)
    def Save(self):
        self.load()
        _db = get_IRES_coll()
        if '_id' in dir(self):
            inserted_id = UpdateOne(_db,self)
        else:
            inserted_id = InsertOne(_db,self) 
            self._id=inserted_id
        return inserted_id
    def loadFromJson(self,dbjsondata):
        for (k, v) in dbjsondata.items():
                setattr(self,k,v)

class EmotionData:
    def __init__(self):
        self.Message = None
        self.SessionID = None
        self.Version = None 
        self.Type = None 
        self.Data = None
        self.Data_Raw = None
    def load(self):
        if self.Version is None:
            self.Version = str(Config.Version['EmotionVersion'])
        if self.Type is None:
            self.Type = str(Config.Version['EmotionType'])
        if self.Data is None:
            if self.Message is not None and self.SessionID is not None:
                self.Data,self.Data_Raw = InvokeEmotions(self.Message)
    def MyJson(self):
        return GetJson(self)
    def Save(self):
        self.load()
        _db = get_Emotional_coll()
        if '_id' in dir(self):
            inserted_id = UpdateOne(_db,self)
        else:
            inserted_id = InsertOne(_db,self)
            self._id=inserted_id
        return inserted_id
    def loadFromJson(self,dbjsondata):
        for (k, v) in dbjsondata.items():
                setattr(self,k,v)
    
