from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
import random

wallpaper = ['531880', '1103970', '1939485', '242236', '399161', '1903702', '129731', '270360',
            '716398', '997443', '1169754', '1229861', '747964', '326311', '160107', '313782', '255379',
            '743986', '669996', '1261728', '1040499', '131634', '268533', '235985', '303383']
# Create your views here.
def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect("dashboard")
        else:
            args = {}
            args['wallpaper'] = random.choice(wallpaper)
            return render(request, 'accounts/login.html',{'error':'Username or Password is incorrect!'}, args)
    else:
        args = {}
        args['wallpaper'] = random.choice(wallpaper)
        return render(request, 'accounts/login.html', args)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        args = {}
        args['wallpaper'] = random.choice(wallpaper)
        return render(request, 'accounts/login.html', args)
