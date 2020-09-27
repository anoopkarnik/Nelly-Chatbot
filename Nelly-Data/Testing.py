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

#cd = ChatData('ABCD1234')
#result =cd.GetChat()
#cd.Message = 'Hello, I am going to gym today and it is special for me'
#cd.Response ='Response from Nelly'

#inserted_id=cd.Save()
#print(inserted_id)

#a1 =cd.MyJson()
#a1 =del_none(json.loads(cd.MyJson()))

#db=db_Ops()
#db.SaveChat(cd)

#db = get_data_coll()
#x = GetJson(cd)

#insvalue = db.insert_one(a1).inserted_id
#print(insvalue)

#thrSave = threading.Thread(target=UpdateOne,args=(_db,self))
#            thrSave.start()

#backgroundProcess = Process(target=InvokeGet,args=(Url,data), daemon=True)
    #backgroundProcess.start()

#server='3.135.101.28'
#port=8000
#sessionId='ABCD1234'
#session_info = json.dumps({'Message':'Hello','Response':'Test'},sort_keys=True,separators=(',', ': '))
#response_text = requests.post('http://{}:{}/ABCD1234'.format(server,port),json=session_info)
#print(response_text.status_code)

#if response_text.status_code == 200:
#    session_response = response_text.json()["data"]
#    for item in session_response["session_list"]:
#        print(item)