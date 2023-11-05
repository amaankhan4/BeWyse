from django.shortcuts import render
from django.http import HttpResponse
from .db_connect import user_collec,customTokens
import random,string,json
from .firebase_auth import create_custom_id


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
    
def edit(request,username):
    user_token = customTokens.find_one({'username':username},{'_id':0})
    if user_token:
        email =  user_collec.find_one({'username':username},{'email':1,'_id':0}).get('email')
        password =  user_collec.find_one({'username':username},{'password':1,'_id':0}).get('password')
        first_name = user_collec.find_one({'username':username},{'first_name':1,'_id':0}).get('first_name')
        last_name = user_collec.find_one({'username':username},{'last_name':1,'_id':0}).get('last_name')
        if request.method == "POST":
            updated_fn = request.POST.get('first_name')
            updated_ln = request.POST.get('last_name')
            updated_un = request.POST.get('username')
            if updated_fn == first_name and updated_ln == last_name and updated_un == username:
                return HttpResponse('',status=200)
            elif user_collec.find_one({'username':updated_un}) and updated_un != username:
                return HttpResponse(f"User already exist with the username ${updated_un}")
            else:
                user_collec.find_one_and_replace({'username':username},{'username':updated_un,'last_name':updated_ln,'first_name':updated_fn,'email':email,'passowrd':password})
            json_data = json.dumps({'username':updated_un,'email':email,'full_name':(updated_fn+" "+updated_ln)})

            return HttpResponse(json_data)

    else:
        return HttpResponse('UNAUTHORIZED',status=401)

    return render(request,'accounts/profile_edit.html',{'username':username,'first_name':first_name,'last_name':last_name})
