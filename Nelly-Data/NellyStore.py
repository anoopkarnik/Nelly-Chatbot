import Config
import pymongo
from pymongo.collection import ReturnDocument
from Utility import *

#class NellyStore(object):

def get_db():
        constring = "mongodb+srv://{0}:{1}@{2}/{3}?retryWrites=true&w=majority"
        client = pymongo.MongoClient(constring.format(
            Config.DATABASE_CONFIG['UserName'],
            Config.DATABASE_CONFIG['Password'],
            Config.DATABASE_CONFIG['Host'],
            Config.DATABASE_CONFIG['DBName']
            ))
        return client[Config.DATABASE_CONFIG['Collection']]

def get_data_coll():
        dbclient = get_db()
        return dbclient[Config.DATABASE_CONFIG['ChatData']]

def get_seq_coll():
        dbclient = get_db()
        return dbclient[Config.DATABASE_CONFIG['Sequence']]

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
    return db.insert_one(data.MyJson()).inserted_id

def UpdateOne(db,data):
    from bson.objectid import ObjectId
    _idValue =data.__dict__.get('_id')
    jsonValue =data.MyJson()
    del jsonValue['_id']
    db.find_one_and_update(            
    {"_id" : ObjectId(_idValue)},
    {"$set": jsonValue },upsert=True)
    return _idValue

def __InsertMany(self,db,data):
    db.insert_many(data)

def __UpdateMany(self,db,data):
    db.update_many(data)