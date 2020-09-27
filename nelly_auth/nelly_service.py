import requests
import json
import logging
import uuid
import os
import sys
import traceback
import urllib.request
import datetime
import time
from flask import Flask, render_template,request, make_response, jsonify, redirect
from flask_restful import Api,Resource
from jose import jwk, jwt
from waitress import serve
from jose.utils import base64url_decode 
from flask_mysqldb import MySQL

app = Flask(__name__) 
FLASK_DEBUG = 1

prev_path = os.path.split(os.getcwd())[0]
log_filename = 'nelly_services.log'
logging.basicConfig(filename=log_filename,format='%(asctime)s %(message)s',filemode='w') 
logger = logging.getLogger() 
logger.setLevel(logging.DEBUG) 

##Retrieve DB connection details from the configuration file
def mysql_details():
    with open('config.json') as config_file:
        data = json.load(config_file)
        app.config['MYSQL_HOST'] = data['MYSQL_HOST']
        app.config['MYSQL_USER'] = data['MYSQL_USER']
        app.config['MYSQL_PASSWORD'] = data['MYSQL_PASSWORD']
        app.config['MYSQL_DB'] = data['MYSQL_DB']
        app.config['MYSQL_PORT'] = data['MYSQL_PORT']
        
mysql_details()
#Creating User rest API's to save, update and read data from the database
api = Api(app)
mysql = MySQL(app)

class User(Resource): 
    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource

    def get(self):
        try:
            customer_email = request.args.get('customer_email')
            cur = mysql.connection.cursor()
            query_string = "select * from user where customer_email = %s and delete_flag = 0"
            cur.execute(query_string,(customer_email,))
            user_list = [list(user) for user in cur.fetchall()]
            if not user_list:
                logger.debug("No data in database with the customer email given")
                return make_response(jsonify(message="No data in database"),404)
            else:
                customer_email = user_list[0][3]
                id_token = user_list[0][4]
                session_id = user_list[0][1]
                user_info_data = {'customer_email': customer_email,'id_token':id_token,'session_id':session_id}
                return make_response(jsonify(data = user_info_data),200)
        except:
            traceback.print_exc(file=sys.stdout)

    # Corresponds to POST request
    def post(self): 
        try:
            data = request.get_json(force=True)
            cur = mysql.connection.cursor()
            jsonified_data = json.loads(data)
            session_id = jsonified_data['session_id']
            user_uuid = jsonified_data['user_uuid']
            customer_email = jsonified_data['customer_email']
            id_token = jsonified_data['id_token']
            access_token = jsonified_data['access_token']
            cur.execute("insert into user(session_id,user_uuid,customer_email,id_token,access_token) values (%s,%s,%s,%s,%s)", (session_id,user_uuid,customer_email,id_token,access_token))
            mysql.connection.commit()
            cur.close()
            return make_response(jsonify(data),200) 
        except:
            traceback.print_exc(file=sys.stdout)
    
    def put(self):
        try:
            data = request.get_json(force=True)
            cur = mysql.connection.cursor()
            jsonified_data = json.loads(data)
            customer_email = jsonified_data['customer_email']
            cur.execute("update user set delete_flag = 1 where customer_email= %s",(customer_email,))
            mysql.connection.commit()
            cur.close()
            return make_response(jsonify(data),200)  
        except:
            traceback.print_exc(file=sys.stdout)


# adding the defined resources along with their corresponding urls
api.add_resource(User,'/user')

def get_key_details(region,userpool_id):
    region = region
    userpool_id = userpool_id
    keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)
    with urllib.request.urlopen(keys_url) as f:
        response = f.read()
        keys = json.loads(response.decode('utf-8'))['keys']
    return keys

@app.route('/validate_user')
def validate_user():
    data = request.get_json(force=True)
    jsonified_data = json.loads(data)
    token = jsonified_data['token']
    keys = get_key_details(jsonified_data['region'],jsonified_data['userpool_id'])
    client_id = jsonified_data['client_id']
    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('Public key not found in jwks.json')
        return make_response(jsonify(message="Public key not found in jwks.json"),400)
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        return make_response(jsonify(message="Signature verification failed"),400)
    print('Signature successfully verified')
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        return make_response(jsonify(message="Token has expired"),403)
    # and the Audience (use claims['client_id'] if verifying an access token)
    if claims['aud'] != client_id:
        print('Token was not issued for this audience')
        return make_response(jsonify(message="Token was not issued for this audience"),400)
    # now we can use the claims
    return make_response(jsonify(message="Valid User",data ={"sessionId":uuid.uuid4()}),200)

@app.route('/validate_sessionId')
def validate_sessionId():
    try:
        session_id = request.headers.get('session_id')
        cur = mysql.connection.cursor()
        query_string = "select * from user where session_id = %s and delete_flag = 0"
        cur.execute(query_string,(session_id,))
        user_list = [list(user) for user in cur.fetchall()]
        if not user_list:
            logger.debug("No data in database with given session Id")
            return make_response(jsonify(message="No data in database with given session Id"),400)
        else:
            session_id = user_list[0][1]
            return make_response(jsonify(message="Valid Session Id",data={"session_id":session_id}),200)
    except:
        traceback.print_exc(file=sys.stdout)

@app.route('/get_sessionId')
def get_sessionId():
    try:
        sessions_list = []
        sessionid_list = []
        data = request.get_json(force=True)
        jsonified_data = json.loads(data)
        session_id = jsonified_data['sessionId']
        records_number = jsonified_data['records_number']
        cur = mysql.connection.cursor()
        query_string = "select customer_email from user where session_id = %s"
        cur.execute(query_string,(session_id,))
        customer_email = cur.fetchone()
        if customer_email is None:
            logger.debug("No data in database with given session Id")
            return make_response(jsonify(message="No data in database with given session Id"),400)
        else:
            query_string = "select session_id from user where customer_email = %s order by created_date"
            cur.execute(query_string,(customer_email,))
            for session in cur.fetchall():
                sessions_list.append(session[0])
            if not sessions_list:
                logger.debug("No sessions list with given customer_email")
                return make_response(jsonify(message="No sessions list with given customer_email"),400)
            else:
                for records in range(len(sessions_list)-1-records_number,len(sessions_list)-1):
                    sessionid_list.extend(sessions_list[records])
                return make_response(jsonify(message="Sessions List",data={"session_list":sessionid_list}),200)      
    except:
        traceback.print_exc(file=sys.stdout)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
