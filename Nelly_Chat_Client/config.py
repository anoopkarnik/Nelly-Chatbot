class FullLocalConfig(object):
    MODEL = "90M"
    CLIENT_ID = "5vi511lkkr21dghs37ls4ggd7i"
    REDIRECT_URI = "http://localhost:5000/"
    REGION = "us-east-2"
    USERPOOL_ID = "us-east-2_NuxwnIrdn"
    SERVICE_ENDPOINT = "0.0.0.0"
    SERVICE_PORT = 8080
    COGNITO_AUTHDOMAIN = "https://nellydev.auth.us-east-2.amazoncognito.com"
    CORE_ENDPOINT ="0.0.0.0"
    DATA_ENDPOINT = "0.0.0.0"
    DATA_PORT = 8000
    
class CoreLocalConfig(object):
    MODEL = "90M"
    CLIENT_ID = "7ujltubvsf6mg1ntdor4ujvlli"
    REDIRECT_URI = "https://3.135.101.28:5000/"
    REGION = "us-east-2"
    USERPOOL_ID = "us-east-2_Bgj4PmSPQ"
    SERVICE_ENDPOINT = "3.135.101.28"
    SERVICE_PORT = 8080
    COGNITO_AUTHDOMAIN = "https://nellydev.auth.us-east-2.amazoncognito.com"
    CORE_ENDPOINT ="0.0.0.0"
    DATA_ENDPOINT = "0.0.0.0"
    DATA_PORT = 8000
    
class ServiceLocalConfig(object):
    MODEL = "90M"
    CLIENT_ID = "7ujltubvsf6mg1ntdor4ujvlli"
    REDIRECT_URI = "https://3.135.101.28:5000/"
    REGION = "us-east-2"
    USERPOOL_ID = "us-east-2_Bgj4PmSPQ"
    SERVICE_ENDPOINT = "0.0.0.0"
    SERVICE_PORT = 8080
    COGNITO_AUTHDOMAIN = "https://nellydev.auth.us-east-2.amazoncognito.com"
    CORE_ENDPOINT ="3.137.118.10"
    DATA_ENDPOINT = "0.0.0.0"
    DATA_PORT = 8000
    
class ClientLocalConfig(object):
    MODEL = "90M"
    CLIENT_ID = "5vi511lkkr21dghs37ls4ggd7i"
    REDIRECT_URI = "http://localhost:5000/"
    REGION = "us-east-2"
    USERPOOL_ID = "us-east-2_NuxwnIrdn"
    SERVICE_ENDPOINT = "3.135.101.28"
    SERVICE_PORT = 8080
    COGNITO_AUTHDOMAIN = "https://nellydev.auth.us-east-2.amazoncognito.com"
    CORE_ENDPOINT ="3.137.118.10"
    DATA_ENDPOINT = "0.0.0.0"
    DATA_PORT = 8000

class ProdConfig(object):
    MODEL = "90M"
    CLIENT_ID = "7ujltubvsf6mg1ntdor4ujvlli"
    REDIRECT_URI = "https://18.222.10.164:5000/"
    REGION = "us-east-2"
    USERPOOL_ID = "us-east-2_Bgj4PmSPQ"
    SERVICE_ENDPOINT = "3.20.182.221"
    SERVICE_PORT = 8080
    COGNITO_AUTHDOMAIN = "https://nellynerv.auth.us-east-2.amazoncognito.com"
    CORE_ENDPOINT ="3.129.71.156"
    DATA_ENDPOINT = "0.0.0.0"
    DATA_PORT = 8000
    
class Config(object):
#     ChatStore = 'http://3.20.182.221:8000'
#     AuthServer = '3.135.101.28:8080'
#     ChatStore = 'http://172.26.13.187:8000'
#     AuthServer = '10.0.1.161:8080'
    ChatStore = 'http://0.0.0.0:8000'
    AuthServer = '0.0.0.0:8080'
