from django.shortcuts import render,redirect
from django.http import HttpResponse
from .db_connect import user_collec,customTokens
import random,string,json
from .firebase_auth import create_custom_id,checkValidity


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        user_data = {
            'email': email,
            'password': password,
            'first_name': firstName,
            'last_name': lastName
        }
        suffix = ''.join(random.choices(string.ascii_lowercase,k=6))
        username = 'user_' + (firstName.lower()[0:2]+lastName.lower()).replace(' ','') + suffix
        user_data['username'] = username
        error_mssg = Validation(user_data)
        if error_mssg is not None:
            return HttpResponse(error_mssg)
        user_collec.insert_one(user_data)
        response = {
            'username':username,
            'email':email
        }
        json_dump = json.dumps(response,indent=4)
        return HttpResponse(json_dump)
    return render(request,"accounts/register.html")


def Validation(user_data):
    if user_collec.find_one({'username':user_data['username']}):
        return "A user with that username already exists"
    
    for data in user_data.values():
        if len(data) > 100:
            return "Only 100 characters are allowed for a field"


    if len(user_data['email']) == 0 or len(user_data['password']) == 0:
        return "Email and password are required"
    
    if len(user_data['password']) < 8:
        return "This password is too short. It must contain at least 8 characters"

    return None


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if user_collec.find_one({'username':username,'password':password}):
            custom_token = create_custom_id(username)
            return HttpResponse(custom_token)
        else:
            return HttpResponse('Username or password is invalid',status=404)
    return render(request,'accounts/login.html')


def view(request,username):
    user_token = customTokens.find_one({'username':username},{'_id':0})
    if user_token:
        user_data = user_collec.find_one({'username':username},{"_id":0,"password":0})
        fullName = user_data.get('first_name') + " " + user_data.get('last_name')
        user_data['full_name'] = fullName
        del user_data['last_name']
        del user_data['first_name']
        json_data = json.dumps(user_data)
        return HttpResponse(json_data)
    else:
        return HttpResponse('UNAUTHORIZED',status=401)  
    
def edit(request):
    return HttpResponse("Success",status=200)
