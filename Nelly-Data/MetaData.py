# Chat Meta Data Structure
import json
from Utility import *
from NellyStore import *
from datetime import datetime
from Config import *

class ChatData:
    def __init__(self,SessionID):
        self.SessionID=SessionID
        self.IRESData = None
        self.ModelType = None
        self.ModelVersion = None
        self.TimeStamp = None
        self.Message = None
        self.Response = None
        self.EmotionData = None
        self.EmotionData_Raw = None

#Property IRESData
    def Add_IRESData(value):
        IRESData.append(value)
    def Remove__IRESData(value):
        IRESData.remove(value)
    def Clear_IRESData():
        IRESData.Clear()

    def UpdateIRES(self):
        return None
        #if self.IRESData is None:
        #    _IRESData =InvokeOpenIE(self.Message)
        #    if len(_IRESData) > 0 :
        #        self.IRESData=_IRESData

    def UpdateEmotional(self):
        return None
        #if self.EmotionData is None:
        #    self.EmotionData,self.EmotionData_Raw=InvokeEmotions(self.Message)

    def MyJson(self):
        return GetJson(self)

    def Save(self):
        t1 = threading.Thread(name='OpenIE', target=self.UpdateIRES)
        t2 = threading.Thread(name='Emotion', target=self.UpdateEmotional)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.TimeStamp=str(datetime.utcnow())
        if self.ModelType is None:
            self.ModelType = Config.Version['ModelType']
        if self.ModelVersion is None:
            self.ModelVersion = Config.Version['ModelVersion']

        _MyJson = self.MyJson()
        _db = get_data_coll()

        if '_id' in dir(self):
            inserted_id=UpdateOne(_db,self)
        else:
            inserted_id=InsertOne(_db,self) 
        return inserted_id

    def GetChat(self):
        _db = get_data_coll()
        return _db.find({'SessionID':self.SessionID})