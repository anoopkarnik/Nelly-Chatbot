import requests
import json 

API_Server = {
#     'ChatStore' : 'http://3.20.182.221:8000',
    #'AuthServer': '3.135.101.28:8080'
    #'ChatStore' : 'http://172.26.13.187:8000',
#     'AuthServer': '10.0.1.161:8080'
    'ChatStore' : 'http://0.0.0.0:8001',
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

def GetChatHistory(SessionID):
    prevSessionList=GetPreviousSessionID(SessionID)
    sessions_list = []
    try:
        if prevSessionList is not None and len(prevSessionList) != 0:
            for value in range(len(prevSessionList)-1, -1, -1):
                prevSessionId = prevSessionList[value]
                response = getChat(prevSessionId)
                sessions_list.append(response.json())
        else:
            print('previous session is EMPTY for session id :' + str(SessionID))
            print('getting history from current session')
            response = getChat(SessionID)
            sessions_list.append(response.json())
    except BaseException as e:
        print(e)
    return sessions_list

def getChat(sessionId):
    Url = API_Server['ChatStore'] + '/{0}'
    Url = Url.format(sessionId)
    print('Sending request to get chat for previous session id: ' + str(sessionId))
    response = requests.get(url=Url)
    print('Received response for the get chat request: ' + str(response.json()))
    return response

def GetPreviousSessionID(sessionId):
    headers = {'Content-type': 'application/json'} 
    try:
        session_info = json.dumps({'sessionId' : sessionId, 'records_number': 5}, sort_keys=True,separators=(',', ': '))
        print('trying to get previous session id from current session : ' + str(session_info))
        response_text = requests.get('http://{}/get_sessionId'.format(API_Server['AuthServer']), json=session_info, headers = headers)
        if response_text.status_code == 200:
            session_response = response_text.json()["data"]
            print('received response from GetPreviousId API : '+ str(session_response))
            return session_response["session_list"]
    except BaseException as e:
        print(e)
