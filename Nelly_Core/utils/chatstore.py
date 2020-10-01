import requests
import json 

API_Server = {
    #'ChatStore' : 'http://3.135.101.28:8000',
    #'AuthServer': '3.135.101.28:8080'
#     'ChatStore' : 'http://10.0.1.161:8000',
#     'AuthServer': '10.0.1.161:8080',
    'ChatStore' : 'http://0.0.0.0:8000',
    'AuthServer': '0.0.0.0:8080'
    }

def SaveChat(SessionID,Message,Response):
    try:
        Url = API_Server['ChatStore'] + '/{0}'
        Url = Url.format(SessionID)
        data ={
            'Message': Message,
            'Response' : Response
            }
        requests.post(url = Url,data=json.dumps(data))
        print('sent to save chat: '+ data.__str__())
    except BaseException as e:
        print(e)

def GetChat(SessionID):
    prevSessionList=GetPreviousSessionID(SessionID)
    sessions_list = []
    try:
        if len(prevSessionList) != 0:
            for sessionId in range(len(prevSessionList),0,-1):
                Url = API_Server['ChatStore'] + '/{0}'
                Url = Url.format(sessionId)
                print('Sending request to get chat for previous session id: '+str(sessionId))
                r = requests.get(url = Url)
                print('Received response for the get chat request: ' + str(r.json()))
                sessions_list.append(r.json())
            return sessions_list        
        else:
            print('previous session is EMPTY for session id :' + str(SessionID))
            return None
    except BaseException as e:
        print(e)

def GetPreviousSessionID(sessionId):
    headers = {'Content-type': 'application/json'} 
    try:
        session_info = json.dumps({'sessionId':sessionId,'records_number':2},sort_keys=True,separators=(',', ': '))
        print('trying to get previous session id from current session : ' + str(session_info))
        response_text = requests.get('http://{}/get_sessionId'.format(API_Server['AuthServer']),json=session_info,headers=headers)
        if response_text.status_code == 200:
            session_response = response_text.json()["data"]
            print('received response from GetPreviousId API : '+ str(session_response))
            return session_response["session_list"]
    except BaseException as e:
        print(e)
