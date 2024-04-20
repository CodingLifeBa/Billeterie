from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth import authenticate
# Create your views here.

User = get_user_model()

def signup(request):
    if request.method == "POST":
        username= request.POST.get("username")
        password = request.POST.get("password")
        user=User.objects.create_user(username=username,
                                password=password)
        
        login(request, user)
      
        return redirect('home')

    return render(request, 'accounts/signup.html')




def login_user(request):
    if request.method == "POST":
        username= request.POST.get("username")
        password = request.POST.get("password")

        user =authenticate(username=username, password=password)
        if user:
            login(request,user)
            return redirect('home')
    
    return render(request, 'accounts/login.html')



def logout_user(request):
    logout(request)
    return redirect('home')