from NellyStore import * 
from bson.json_util import *
from openie import *
from MetaData import *
from datetime import datetime
import json
from bson import json_util

#print(getsequence_nextval('UserID'))

#seqdb = get_seq_coll()
#x = seqdb.find_one()
#x['id'] = 2018
#del x['_id']
#p1 = db_Ops()
#p1.save(x)

#import os
#cur_path = os.path.dirname(__file__)
# new_path = os.path.relpath('..\\subfldr1\\testfile.txt', cur_path)

#with StanfordOpenIE() as client:
#    with open('D:\\Work\\Nerv\\Nelly-Data\\src\\test1.txt', 'r', encoding='utf8') as r:
#        corpus = r.read().replace('\n', ' ').replace('\r', '')
#        triples_corpus = client.annotate(corpus[0:50000])
#        print('Corpus: %s [...].' % corpus[0:80])
#        print('Found %s triples in the corpus.' % len(triples_corpus))
#        for triple in triples_corpus:
#            print('|-', triple)


#print(datetime.utcnow())
cd = ChatData()
cd.SessionID= 'ABCD12345'
#result =cd.GetChat()
cd.Message = 'Hello, I am going to gym today and it is special for me'
cd.Response ='Response from Nelly'
inserted_id=cd.Save()
print("Inserted:{0},{1}".format(inserted_id,str(datetime.utcnow())))

#a1 =cd.MyJson()
#a1 =del_none(json.loads(cd.MyJson()))

#db=db_Ops()
#db.SaveChat(cd)

#db = get_data_coll()
#x = GetJson(cd)

#insvalue = db.insert_one(a1).inserted_id
#print(insvalue)
#thrSave = threading.Thread(target=UpdateOne,args=(_db,self))
#thrSave.start()
#backgroundProcess = Process(target=InvokeGet,args=(Url,data), daemon=True)
#backgroundProcess.start()



#session_info = json.dumps({'sessionId':sessionId,'records_number':2},sort_keys=True,separators=(',', ': '))
#response_text = requests.get('http://{}:{}/get_sessionId'.format(server,port),json=session_info,headers=headers)
#if response_text.status_code == 200:
#    session_response = response_text.json()["data"]
#    print(session_response)
        
    #def __GetHistoricIRES(self):
    #    _db = get_IRES_coll()
    #    self.His_IRES = _db.find_one({'$and': 
    #                     [{'SessionID':self.SessionID},
    #                      {Config.Version['IRESType']:{'$ne':self.IRESType}},
    #                      {Config.Version['IRESVersion']:{'$ne':self.IRESVersion}}]})

    #def __GetHistoricEmotional(self):
    #    _db = get_Emotional_coll()
    #    self.His_Emotion = _db.find({'$and': 
    #                     [{'SessionID':self.SessionID},
    #                      {Config.Version['EmotionType']:{'$ne':self.EmotionType}},
    #                      {Config.Version['EmotionVersion']:{'$ne':self.EmotionVersion}}]})


#EData,EData_Raw =InvokeEmotions("Hello, I am very happy today, I am very Angry")
#print(EData)
#print(EData_Raw)
#print("satheesh")


#result =getChatMessages('ABCD1234')
#chatlist = [chat for chat in result]
#c = ChatData('ABCD12345')
#c.Message = "Hello, I am going to play hockey today, I am very excited"
#c.Response = "No Response"
#c.Save()
#print("Printed New Object")

#cu =ChatUtility()
#chatobj = cu.GetChatObject('5f70b4b4f9e344efd2c0b651')
#chatobj.Save()
#print(chatobj.MyJson())
#print("Printed Old Object")

#chatobj1=json_util.dumps(chatobj,cls=ChatDataEncoder, indent=4)
#chatjson = json.loads(chatobj1)
#_idValue =chatjson.get('_id')
#del chatjson['_id']
#studentObj = ChatData(**chatjson)
#studentObj._id = _idValue
#studentObj.Message ="Hello, I am going to gym today and it is special for me-Modified"
#studentObj.Save()
#_idValue =data.__dict__.get('_id')
#    jsonValue =data.MyJson()
#    del jsonValue['_id']
#    db.find_one_and_update(            
#    {"_id" : ObjectId(_idValue)},




#resultDict =json.loads(chatobj1, object_hook=json_util.object_hook)
#studentObj = ChatData(**resultDict)
#print("Object type is: ", type(studentObj))
#print(chatobj)
