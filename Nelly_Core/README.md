# Nelly

LifeLong AI Counselor

## Pre-Requisites

1) -   Install Python3 (>=3.7)
   -   pip3
   -   Setup virtual env of python3 to run this project in.
       instructions here - <https://opensource.com/article/19/5/python-3-default-mac>
   -   IDE - Atom or PyCharm
   -   nice-to-have: zsh terminal setup up.


2) - or If you have anaconda installed
   - conda create -n nelly python=3.7

## Setup Instructions

-   Run: pip3 install -r requirements.txt
-   pip3 install tornado

-   ##### Note:
    if there is an error about **MACOSX_DEPLOYMENT_TARGET** mismatch, set it to what was the configured version.
    ```
    export MACOSX_DEPLOYMENT_TARGET=10.15
    ```

-   Download the model from below location.
    https://drive.google.com/drive/folders/1v5me2HPpp7UmnERXkc7nB-H0WCf-iOUx?usp=sharing
    
-   Copy/Move it to data/models/blender/blender_3B for 3B model and Copy/Move it to data/models/blender/blender_90M for 90M model

-   Run
    ```
    python3 setup.py install
    ```
-   Change all the paths in the model.opt file in the blender_90M folder to the path of folders to their locations in your local drive
-   Run the following command to use the 90Mil model.
    
    In first terminal to run the server 
    ```
    export PYTHONPATH='location of Nelly_Core in your local drive (ex - /home/anoop/Downloads/Nelly_core)'
    cd Nelly_Core/chat_service/core
    python3 run.py blender/blender_90M/model
    
    ```
    In second terminal to run the web app
    ```
    export PYTHONPATH='location of Nelly_Core in your local drive (ex - /home/anoop/Downloads/Nelly_Core)'
    python3 Nelly_Core/chat_service/client/client.py
    
    ```
    Start and keep running chat-server core, before starting the client.
