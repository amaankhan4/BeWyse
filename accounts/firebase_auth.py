import firebase_admin
from firebase_admin import credentials,auth
from .db_connect import customTokens
import jwt,time

cred = credentials.Certificate("C:/Users/ak716/OneDrive/Documents/MAXON/BeWyse/accounts/bewyse-9d0a5-firebase-adminsdk-e7bci-917f49b816.json")

app = firebase_admin.initialize_app(cred)

def create_custom_id(username):
    if customTokens.find_one({'username':username}):
        data = customTokens.find_one({'username':username})
        custom_token = data.get('custom_token')
        if checkValidity(custom_token):
            return custom_token
        else:
            newToken = auth.create_custom_token(username)
            customTokens.replace_one({'username': username}, {'username':username,'custom_token': newToken})
            return newToken
    else:
        token = auth.create_custom_token(username)
        customTokens.insert_one({'username':username,'custom_token':token})
        return token
    

def checkValidity(custom_token):
    try:
        decoded_token = jwt.decode(custom_token)
        exp = decoded_token.get('exp',0)
        if exp:
            currTime = time.time()
            if exp > currTime:
                return True
            else:
                return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
