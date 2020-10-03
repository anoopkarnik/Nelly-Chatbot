import requests

API_Server = {
    #'ChatStore' : 'http://127.0.0.1:8000'
#     'ChatStore' : 'http://3.20.182.221:8000/'
    'ChatStore' : 'http://0.0.0.0/'
    }

def SaveChat(SessionID,Message,Response):
    Url = API_Server['ChatStore'] + '/{0}'
    Url = Url.format(SessionID)
    data ={'Message': Message,'Response':Response}
    requests.post(url = Url, params = data)

def GetChat(SessionID):
    Url = API_Server['ChatStore'] + '/{0}'
    Url = Url.format(SessionID)
    r = requests.get(url = Url)
    return r.json()
