from django.shortcuts import render
from django.http import HttpResponse
from .db_connect import user_collec
import random,string,json
import firebase_admin

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
    return render(request,'accounts/login.html')



def view(request):
    return HttpResponse("Success",status=200)
    
def edit(request):
    return HttpResponse("Success",status=200)
