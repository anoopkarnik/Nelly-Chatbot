## Setup Instructions

conda install pytorch torchvision cpuonly -c pytorch

-   Run pip3 install -r requirements.txt

## Configuration Changes
	Config.py

    # Port configuration for WSGI Server
    # Present Configuration is 8000
    'Port':'8000'

    # Application connects to MongoDB
    # Application use dnspython  connectivity
    # Current Value
    'Host': 'cluster0.36zjq.mongodb.net',
    'DBName': 'admin',
    'UserName': 'dbkumar_1976',
    'Password': 'DBKUMAR_1976',
    'Collection' : 'NellyData',

    'Sequence' : 'seqs',
    # ChanData is the List/Document name for storing all chathistory message
    'ChatData' : 'Chat'

    # Application Version 
    'ModelType':'M1',
    'ModelVersion':'V1'

## Consuming Data Service
   
    # ABCD1234 is a SessionID of the user
    # Save Information
    cd = ChatData('ABCD1234')
    cd.Message = 'Hello, I am going to gym today and it is special for me'
    cd.Response ='Response from Nelly'
    inserted_id=cd.Save()
    print(inserted_id)

    # Getting all old Chat information per session
    cd = ChatData('ABCD1234')
    result =cd.GetChat()