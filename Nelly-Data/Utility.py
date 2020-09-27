import json
import requests
import nltk
import threading
from bson.json_util import dumps
from openie import StanfordOpenIE
from transformers import pipeline
#nltk.download('punkt')
#classifier = pipeline("zero-shot-classification")

def InvokeOpenIE(*params):
    with StanfordOpenIE() as client:
        return client.annotate(params[0])

def InvokeEmotions(data):
    data = [data]
    emotion_labels = ['neutral','joy','sadness', 'anger', 'fear', 'surprise','disgust']
    new_data=[]
    for text in data:
        new_data.extend(nltk.sent_tokenize(text))
    output=[]
    output_raw=[]
    for message in new_data:
        temp_emotion_dict={}
        temp_emotion_dict['message'] = message
        result = classifier(message,emotion_labels)
        if (result['labels'][0]=='surprise' and result['scores'][0]<=0.55): #Since the model is biased towards 'surprise' hence added this condition to improve the accuracy  
            temp_emotion_dict['emotion'] = result['labels'][1]
        else:
            temp_emotion_dict['emotion'] = result['labels'][0]
        output.append(temp_emotion_dict)
        output_raw.append(result)
    return json.dumps(output),json.dumps(output_raw)

def GetJson(data,RemoveNone=True):
    jsonValue = json.dumps(data, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    if RemoveNone == True:
        jsonValue = RemoveNull(json.loads(jsonValue))
    return jsonValue
    
def RemoveNull(d):
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d

def InvokeGet(Url,data):
    r = requests.get(url = Url, params = data) 
    return r.json()

def InvokePost(Url,data):
    r = requests.post(url = Url, params = data) 
    return r.text 

def InvokeGetAsync(Url,data):
    thrSave = threading.Thread(target=InvokeGet,args=(Url,data))
    thrSave.start()

def InvokePostAsync(Url,data):
    thrSave = threading.Thread(target=InvokePost,args=(Url,data))
    thrSave.start()

    



