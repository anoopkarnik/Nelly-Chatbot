# config.py
Http_Config = {
    'Port':'8001'
    }

DATABASE_CONFIG = {
    #'Host': 'mongodb+srv://dbkumar_1976:DBKUMAR_1976@cluster0.36zjq.mongodb.net/admin?retryWrites=true&w=majority',
    'Host' : 'mongodb://localhost:27017/',
    'DBName': 'admin',
    'UserName': 'dbkumar_1976',
    'Password': 'DBKUMAR_1976',
    'Collection' : 'NellyData',
    'Sequence' : 'seqs',
    'ChatData' : 'Chat',
    'IRESData' : 'IRES',
    'EmotionalData' : 'Emotion'
    }

Version ={
    'IRESType':'IT-1',
    'IRESVersion':'IV-1',
    'EmotionType':'ET-1',
    'EmotionVersion' : 'EV-1'
    }