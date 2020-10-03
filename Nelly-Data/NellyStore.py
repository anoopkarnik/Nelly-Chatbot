import Config
import pymongo
from pymongo.collection import ReturnDocument
from Utility import *
from bson.objectid import ObjectId

def get_db():
        client = pymongo.MongoClient(Config.DATABASE_CONFIG['Host'])
        return client[Config.DATABASE_CONFIG['Collection']]

def get_data_coll():
    dbclient = get_db()
    return dbclient[Config.DATABASE_CONFIG['ChatData']]

def get_seq_coll():
    dbclient = get_db()
    return dbclient[Config.DATABASE_CONFIG['Sequence']]

def get_IRES_coll():
    dbclient = get_db()
    return dbclient[Config.DATABASE_CONFIG['IRESData']]

def get_Emotional_coll():
    dbclient = get_db()
    return dbclient[Config.DATABASE_CONFIG['EmotionalData']]

def getsequence_nextval(seqName):
    seqdb = get_seq_coll()
    doc = seqdb.find_one_and_update(
    filter={'collection':seqName},
    update={'$inc': {'id': 1}},
    fields={'id': 1, '_id': 0},
    upsert=True,
    return_document = ReturnDocument.AFTER
    )
    return int(doc['id'])

def InsertOne(db,data):
    json_data = data.MyJson()
    return db.insert_one(json_data).inserted_id

def UpdateOne(db,data):
    jsonValue =data.MyJson()
    _idValue =str(data.__dict__.get('_id'))
    del jsonValue['_id']
    db.find_one_and_update(            
    {"_id" : ObjectId(_idValue)},
    {"$set": jsonValue },upsert=True)
    return _idValue


def db_getChatBySession(SessionID):
    _db = get_data_coll()
    #result = _db.find({'SessionID':id})
    #chatlist = [chat for chat in result]
    #return chatlist
    return list(_db.find({'SessionID':SessionID}))

def db_getIRESBySession(SessionID):
    _db = get_IRES_coll()
    return list(_db.find({'SessionID':SessionID}))

def db_getEmotionBySession(SessionID):
    _db = get_Emotional_coll()
    return list(_db.find({'SessionID':SessionID}))

def db_getChatByID(_id):
    _db = get_data_coll()
    return _db.find_one({'_id':ObjectId(_id)})

def db_getIRESByID(_id):
    _db = get_IRES_coll()
    return _db.find_one({'_id':ObjectId(_id)})

def db_getEmotionByID(_id):
    _db = get_Emotional_coll()
    return _db.find_one({'_id':ObjectId(_id)})


#def getChatIRES(SessionID, Message:str,Version:str,Type:str):
#    _db=get_IRES_coll()
#    return _db.find_one({'$and': 
#                         [{'SessionID':self.SessionID},
#                          {'Version':Version},
#                          {'Type':Type}]})
# return _db.find({'SessionID':SessionID},{ "_id": 1, "Message": 1, "Response": 1 })

#def getChatEmotion(SessionID:str, Message:str,Version:str,Type:str):
#    _db=get_Emotional_coll()
#    return _db.find_one({'$and': 
#                         [{'SessionID':self.SessionID},
#                          {'Version':Version},
#                          {'Type':Type}]})
