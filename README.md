## a) Pre-Requisites

- Install Anaconda and conda create -n nelly python=3.7
or 
- Install python 3.7  and create a local environment nelly

## b) Setup Instructions

-   git clone these 4 repositories - Nelly_Core, Nelly-Data, nelly_auth and Nelly_Chat_Client
-   Run: pip3 install -r requirements.txt in each of the 4 folders - Nelly_Core, Nelly-Data, nelly_auth and Nelly_Chat_Client
-   Download the 90M model from below location.https://drive.google.com/drive/folders/1v5me2HPpp7UmnERXkc7nB-H0WCf-iOUx?usp=sharing    
-   Copy/Move it to data/models/blender/blender_90M for 3B model and Copy/Move it to Nelly_Core/data/models/blender/blender_90M for 90M model

## c) Development Instructions

#### 1) Core Changes

-   Modify these values in config.py file - Data Services Server and Port, Auth Services Server and Port and Nelly Core Location based on which services you want to run in local.    

#### 2) Chat Client Changes

-   Modify these values in Config class in config.py file - Data Services Server and Port and Auth Services Server and Port 


## d) Running Instructions ( Start services/server which you want to run from local based on instructions below)
    
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
    export FLASK_ENV=total_development/core_development/service_development/client_development/production(based on which server or services you want to test in local)
    cd Nelly_Chat_Client
    python runner.py    
    ```
Open http://localhost:5000 in web browser and sign up and login to your account.
