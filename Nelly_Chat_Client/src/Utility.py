import requests
import json

API_Server = {
    'ChatStore' : 'http://0.0.0.0:8000',
    'AuthServer': '0.0.0.0:8080'
    }


def SaveChat(SessionID,Messsage,Response):
    Url = API_Server['ChatStore'] + '{0}'
    Url = Url.format(SessionID)
    data ={
        'Message': Messsage,
        'Response' : Response
        }
    requests.post(url = Url, params = json.dumps(data))

def GetChat(SessionID):
    prevSession=GetPreviousSessionID(SessionID)
    if prevSession != None: 
        Url = API_Server['ChatStore'] + '/{0}'
        Url = Url.format(prevSession)
        r = requests.get(url = Url) 
        return r.json()
    else:
        return None

def GetPreviousSessionID(SessionID):
    retValue = None
    session_info = json.dumps({'sessionId':SessionID,'records_number':1},sort_keys=True,separators=(',', ': '))
    response_text = requests.get('http://{}/get_sessionId'.format(API_Server['AuthServer']),json=session_info)
    if response_text.status_code == 200:
        session_response = response_text.json()["data"]
        for item in session_response["session_list"]:
            retValue=item
    return retValue
