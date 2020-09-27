class Config(object):
    MODEL = "90M"
    CLIENT_ID = "5vi511lkkr21dghs37ls4ggd7i"
    REDIRECT_URI = "http://localhost:5000/"
    REGION = "us-east-2"
    USERPOOL_ID = "us-east-2_NuxwnIrdn"
    SERVICE_ENDPOINT = "localhost"
    SERVICE_PORT = 8080
    COGNITO_AUTHDOMAIN = "https://nellydev.auth.us-east-2.amazoncognito.com"
    CORE_ENDPOINT ="localhost"

class ProdConfig(Config):
    CLIENT_ID = "7ujltubvsf6mg1ntdor4ujvlli"
    USERPOOL_ID = "us-east-2_Bgj4PmSPQ"
    REDIRECT_URI = "https://3.135.101.28:5000/"
    COGNITO_AUTHDOMAIN = "https://nellynerv.auth.us-east-2.amazoncognito.com"
    CORE_ENDPOINT ="10.0.0.158"
    
 