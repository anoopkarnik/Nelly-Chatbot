# Nelly_Personal

## a) Pre-Requisites

1) -   Install Python3 (>=3.7)
   -   pip3
   -   Setup virtual env of python3 to run this project in.
       instructions here - <https://opensource.com/article/19/5/python-3-default-mac>
   -   IDE - Atom or PyCharm
   -   nice-to-have: zsh terminal setup up.


2) - or If you have anaconda installed
   - conda create -n nelly python=3.7

## b) Setup Instructions

-   git clone this repository.
-   Run: pip3 install -r requirements.txt in each of the 4 folders - Nelly_Core, Nelly-Data, nelly_auth and Nelly_Chat_Client

#### 1) Model Core Changes

-   Download the 90M model from below location.https://drive.google.com/drive/folders/1v5me2HPpp7UmnERXkc7nB-H0WCf-iOUx?usp=sharing    
-   Copy/Move it to data/models/blender/blender_90M for 3B model and Copy/Move it to Nelly_Core/data/models/blender/blender_90M for 90M model

##### Production to local development

-   Change all the paths in the model.opt file in the blender_90M folder to the path of folders to their locations in your local drive
-   Check in Nelly_Core/chat_service/websocket/sockets.py if server is '0.0.0.0' in open_method
-   Check in Nelly_Core/chatstore.py change value of 'ChatStore' : 'http://0.0.0.0:8000' and 'AuthServer': '0.0.0.0:8080'

#### 2) Chat Client Changes
##### Production to local development
-   In Chat_Client/src/Utility.py change value of 'ChatStore' : 'http://0.0.0.0:8000' and 'AuthServer': '0.0.0.0:8080'
-   In Chat_Client/config.py change REDIRECT_URI = "http://localhost:5000/", SERVICE_ENDPOINT = "0.0.0.0", CORE_ENDPOINT ="0.0.0.0"

#### 3) Auth Changes
-   Last line in nelly_auth/services.py from serve(app,host='0.0.0.0',port=8080) to app.run(host='0.0.0.0',port=8080) 

## c) Running Instructions
    
#### 1) In first terminal to run the server 
    ```
    conda activate nelly
    export PYTHONPATH='location of Nelly_Core in your local drive (ex - /home/anoop/Downloads/Nelly_Core)'
    cd Nelly_Core/chat_service/core
    python run.py blender/blender_90M/model
    
    ```
#### 2) In second terminal to start auth services
    ```
    conda activate nelly
    cd nelly_auth
    python nelly_service.py 
    ```
    
#### 3) In third terminal to start data services
    ```
    conda activate nelly
    cd Nelly-Data
    python NellyRoute.py
    ```
    
#### 4) In fourth terminal to run the web app
    ```
    conda activate nelly
    export FLASK_ENV=development
    cd Nelly_Chat_Client
    python runner.py    
    ```
    Open http://localhost:5000 in web browser and sign up and login to your account.
