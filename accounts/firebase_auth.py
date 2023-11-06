import firebase_admin
from firebase_admin import credentials,auth
from .db_connect import customTokens
import time

cred = credentials.Certificate("C:/Users/ak716/OneDrive/Documents/MAXON/BeWyse/accounts/bewyse-9d0a5-firebase-adminsdk-e7bci-917f49b816.json")

app = firebase_admin.initialize_app(cred)

def create_custom_id(username):
    if customTokens.find_one({'username':username}):
        exp = customTokens.find_one({'username':username}).get('exp')
        if checkValidity(exp):
            return customTokens.find_one({'username':username}).get('custom_token')
        else:
            newToken = auth.create_custom_token(username)
            customTokens.replace_one({'username': username}, {'username':username,'custom_token': newToken,'exp':(time.time()+3600)})
            return newToken
    else:
        token = auth.create_custom_token(username)
        exp_time = time.time() + 3600
        customTokens.insert_one({'username':username,'custom_token':token,'exp':exp_time})
        return token
    

def checkValidity(exp):
    currTime = time.time()
    if exp > currTime:
        return True
    else:
        return False
    