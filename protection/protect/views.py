from django.shortcuts import render
from protect.forms import UserForm , UserProfileInfoForms
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import  authenticate, login, logout

# Create your views here.
def index(request):
    return render(request , 'protect/index.html')

@login_required()
def special(request):
    return HttpResponse("You are logged in , Nice!")

@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForms(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True

        else:
            print(user_form.errors , profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForms()
    return render(request , 'protect/registration.html' , {'user_form' : user_form , 'profile_form': profile_form , 'registered' : registered})

def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username , password = password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
                #if the user logs in successfully and the account is active , returns you to the previously loaded index page

            else:
                return HttpResponse("Account not active")
        else:
            print("Someone tried to login and failed")
            print("Username: {} Password: {}".format(username,password))
            return HttpResponse("Inavlid log in details supplied")
    else:
        return render(request, 'protect/login.html')
