import requests,json, threading,uuid, websocket, os, sys, traceback, urllib.request, datetime, time
from flask import Flask, render_template,request, make_response, jsonify, redirect, Blueprint, current_app as app
import jwt 
from src.Utility import GetChatHistory
from waitress import serve
from http import cookies
from src.MessageHandler import *

SHARED = {}
SHARED['websockets'] = {}
SESSION = {}
SESSION['access_token'] ={}

configPath = os.getcwd()

chat_bluePrint = Blueprint('chat_bluePrint',__name__,template_folder='templates', static_folder='static')
FLASK_DEBUG=1

def save_user_details(customer_email,session_id,user_info_data,headers,server,port):
    res_user_get_info = requests.get('http://{}:{}/user?customer_email={}'.format(server,port,customer_email))
    if res_user_get_info.status_code == 200:
        data = res_user_get_info.json()["data"]
        res_user_update_info = requests.put('http://{}:{}/user'.format(server,port),json=json.dumps(data,sort_keys=True,separators=(',', ': ')),headers=headers)
        if res_user_update_info.status_code == 200:
            print("Soft delete of user details done in the database")
        else:
            print("Update operation failed")
            return make_response(jsonify(message = "Update operation failed"))
    res_user_post_info = requests.post('http://{}:{}/user'.format(server,port),json=user_info_data,headers=headers)
    if res_user_post_info.status_code == 200:
        print("User information data successfully inserted in the database")
    elif res_user_post_info.status_code == 400:
        print("Post operation failed as"+res_user_post_info["message"])
        return make_response(jsonify(message = "Post operation failed as"+res_user_post_info["message"]))
    else:
       print("Post operation failed")
       return make_response(jsonify(message = "Post operation failed"))

def get_token(url,data):
    res_token_info = requests.post(url,data=data)
    print(res_token_info.json())
    if (res_token_info.status_code == 200):
        print("Token received from cognito")
        token = json.loads(res_token_info.text)
        id_token = token.get("id_token")
        id_token_payload = jwt.decode(id_token, verify=False)
        customer_email = id_token_payload['email']
        user_uuid = id_token_payload['sub']
        access_token = token.get("access_token")
        refresh_token = token.get("refresh_token")
        return make_response(jsonify(message="Token Received from Cognito",data = {'customer_email':customer_email,'user_uuid':user_uuid,'id_token':id_token,'access_token':access_token,'refresh_token':refresh_token}),200)
    else:
        return make_response(jsonify(message="Couldn't get token from cognito"),400)

@chat_bluePrint.route('/', methods=['GET'])
def index(createNesSessionId = False):
    sessionId = None
    results_list = []
    if (createNesSessionId == False and 'sessionId' in request.cookies):
        sessionId = request.cookies['sessionId']
    cognitoAuthDomain = app.config['COGNITO_AUTHDOMAIN']
    server = app.config['SERVICE_ENDPOINT']
    port = app.config['SERVICE_PORT']
    client_id = app.config['CLIENT_ID']
    redirect_uri = app.config['REDIRECT_URI']
    region = app.config['REGION']
    userpool_id = app.config['USERPOOL_ID']
    cognitoAuthUrl = '{}/login?client_id={}&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri={}'.format(cognitoAuthDomain,client_id,redirect_uri)
    validToken, codeRequired, code_access_token = validateToken(sessionId, cognitoAuthUrl)
    if(codeRequired == True):
         return redirect(cognitoAuthUrl, code=302)
    if(validToken == False):
        headers = {'Content-type': 'application/json'}
        info = {'grant_type':'authorization_code', 'client_id':client_id, 'code':code_access_token,'redirect_uri':redirect_uri}
        try:
            response = get_token('{}/oauth2/token'.format(cognitoAuthDomain),info)
            if(response.status_code == 200):
                response = (response.json).get("data")
                id_token = response["id_token"]
                customer_email = response["customer_email"]
                user_uuid = response["user_uuid"]
                access_token = response["access_token"]
                refresh_token = response["refresh_token"]
                user_token_info = json.dumps({'token':id_token,'client_id':client_id,'region':region, 'userpool_id':userpool_id,'access_token':access_token},sort_keys=True,separators=(',',': '))
                refresh_info = {'grant_type':'refresh_token', 'client_id':client_id, 'refresh_token':refresh_token,'redirect_uri':redirect_uri}
                response_text = requests.get('http://{}:{}/validate_user'.format(server,port),json=user_token_info,headers=headers)
                if response_text.status_code==200:
                    user_token_response = response_text.json()["data"]
                    sessionId = user_token_response["sessionId"]
                    user_info_data = json.dumps({'session_id':sessionId,'customer_email':customer_email,'id_token':id_token,'access_token':access_token,'user_uuid':user_uuid},sort_keys=True,separators=(',', ': '))
                    SESSION['access_token'].update({ sessionId: sessionId })
                    save_user_details(customer_email,sessionId,user_info_data,headers,server,port)
                    history = GetChatHistory(sessionId,'no')
                    if history is not None:
                        for data in history:
                            for messages in data:
                                results_list.append({"Message":messages["Message"],"Response":messages["Response"]})
                elif response_text.status_code == 403:
                    refresh_response = get_token('{}/oauth2/token'.format(cognitoAuthDomain),refresh_info)
                    if(refresh_response.status_code == 200):
                        refresh_response = (refresh_response.json).get("data")
                        id_token = refresh_response["id_token"]
                        customer_email = refresh_response["customer_email"]
                        user_uuid = refresh_response["user_uuid"]
                        access_token = refresh_response["access_token"]
                        refresh_token = refresh_response["refresh_token"]
                        user_token_info = json.dumps({'token':id_token,'client_id':client_id,'region':region, 'userpool_id':userpool_id},sort_keys=True,separators=(',',': '))
                        response_text = requests.get('http://{}:{}/validate_user'.format(server,port),json=user_token_info,headers=headers)
                        user_token_response = response_text.json()["data"]
                        if response_text.status_code == 200:
                            sessionId = user_token_response["sessionId"]
                            user_info_refresh_data = json.dumps({'session_id':sessionId,'customer_email':customer_email,'id_token':id_token,'access_token':access_token,'user_uuid':user_uuid},sort_keys=True,separators=(',', ': '))
                            SESSION['access_token'].update({ sessionId: sessionId })
                            save_user_details(customer_email,sessionId,user_info_refresh_data,headers,server,port)
                            history = GetChatHistory(sessionId,'no')
                            if history is not None:
                                for  item in history:
                                    results_list.append({"Message":item["Message"],"Response":item["Response"]})
                        else:
                            return response_text.json()["message"]
                else:
                    print(response.json["message"])
                    return response.json["message"]
            else:
                return redirect(cognitoAuthUrl)
        except Exception as e:
            print('Failed to get the token: '+ str(e))
            #TODO: show error page?
    else:
         history = GetChatHistory(sessionId,'no')
         if history is not None:
            for data in history:
                for messages in data:
                    results_list.append({"Message":messages["Message"],"Response":messages["Response"]})
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    print(results_list)
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    response = make_response(render_template('index.html',data=results_list))
    _createNewSession(sessionId)
    response.set_cookie("sessionId", sessionId)
    return response

@chat_bluePrint.route("/history/", methods=["Get"])
def getHistory():
    results_list=[]
    sessionId = None
    results_list=[]
    if 'sessionId' in request.cookies:
         sessionId = request.cookies['sessionId']
    if sessionId != None :
         history = GetChatHistory(sessionId,'yes')
         if history is not None:
            for data in history:
                for messages in data:
                    results_list.append({"Message":messages["Message"],"Response":messages["Response"]})
    return make_response (render_template('history.html',data=results_list))

def validateToken(sessionId, cognitoAuthUrl):
    validToken = False
    codeRequired = False
    code_access_token = '2423'
    uri = str(request.url)
    print(uri)
    keyword = 'code='
    access_token = SESSION['access_token'].get(sessionId)
    if(access_token is not None):
        # check for access_token valid or not from the Nelly Services.
        validToken = True
    if(validToken == False):
        code_access_token =  uri.partition(keyword)[2].partition("'>>")[0]
        print(code_access_token)
        print(code_access_token.strip())
        if( not code_access_token.strip()):
            codeRequired = True

    return validToken, codeRequired, code_access_token

def _createNewSession(sessionId):
    model = app.config['MODEL']
    ws = open_new_conn(model, sessionId)
    SHARED['websockets'].update({sessionId: ws})

def _sendMessage(userMessage, sessionId):
    data = {}
    webSocket = None
    print('\n Request text: ' + userMessage)
    data['text'] = userMessage
    if data['text'] == "[DONE]":
        print('[ Closing socket... ]')
        SHARED['websockets'].__getitem__(sessionId).close()
        return webSocket
    webSocket = SHARED['websockets'].get(sessionId)
    if webSocket is None :
        print('webSocket is none')
        return webSocket
    else:
        webSocket.sendMessage(data)

    return webSocket

def _get_sessionId():
    sessionId = None
    if 'sessionId' in request.cookies:
        sessionId = request.cookies['sessionId']
    return sessionId

@chat_bluePrint.route("/logout/", methods=["Get"])
def logoutConnection():
    cognitoAuthDomain = app.config['COGNITO_AUTHDOMAIN']
    client_id = app.config['CLIENT_ID']
    redirect_uri = app.config['REDIRECT_URI']
    sessionId = _get_sessionId()
    if sessionId != None :
        SHARED['websockets'].get(sessionId).close()
        SHARED['websockets'].pop(sessionId)
        print("Closed this connection" +sessionId)
        threading.Thread(name='Reset', target=resetServers)
        cognitoLogoutUrl = '{}/logout?client_id={}&response_type=code&redirect_uri={}&state=STATE&scope=aws.cognito.signin.user.admin+email+openid+phone+profile'.format(cognitoAuthDomain,client_id,redirect_uri)
        return jsonify ({'data':cognitoLogoutUrl})

def resetServers():
    #doing this as a stop gap to reset 3B model
    time.sleep(0.5)
    coreserver = app.config["CORE_ENDPOINT"]
    core_response = requests.get(url='http://{}:5555/Nelly_Core'.format(coreserver))
    chat_server = '0.0.0.0'
    chat_server_response = requests.get(url="http://{}:5555/Nelly_Chat".format(chat_server))

@chat_bluePrint.route("/close/", methods=["Post"])
def closeConnection():
    sessionId = _get_sessionId()
    if sessionId != None :
        SHARED['websockets'].get(sessionId).close()
        SHARED['websockets'].pop(sessionId)
        print("Closed this connection" + sessionId)

@chat_bluePrint.route("/postMessage/", methods=["Post"])
def do_POST():
    """
    Handle POST request, especially replying to a chat message.
    """
    websocket = None
    userMessage = request.get_json()
    sessionId = _get_sessionId()
    if sessionId != None :
        websocket = _sendMessage(userMessage['data'], sessionId)
    if websocket == None:
        return jsonify({'data' : "NoActiveSession / Session closed"})

    model_response = {'id': 'Nelly', 'episode_done': False}
    websocket.Message_available.wait()
    model_response['text'] = websocket.NellyResponse
    websocket.Message_available.clear()
    if model_response['text'] is not None:
        print('\n Request:' + str(userMessage['data']) + '  Response: ' + str(model_response['text']))
    else:
        print('\n Problem:')

    return jsonify({'data' : model_response})

def open_new_conn(model, sessionId):
    server = "localhost"
    port = 34596

    if model is not None:
        if model == '90M':
            server = app.config["CORE_ENDPOINT"]
        elif model == '3B':
            server = "3.137.118.10"
        elif model == '9B':
            server = "3.137.118.10"
    print("Connecting to http://{}:{}".format(server, port))
    ws = MessageHandler(model, SESSION["access_token"].get(sessionId), server)
    return ws
