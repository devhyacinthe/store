from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import render, redirect

# Create your views here.
User = get_user_model()


def login_user(request):
    if request.method == "POST":
        # Connecter l'utilisateur
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')

    return render(request, 'acounts/login.html')


def signup(request):
    if request.method == "POST":
        # traitement du formulaire
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('index')

    return render(request, 'acounts/signup.html')


def logout_user(request):
    logout(request)
    return redirect('index')
