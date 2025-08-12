from django.shortcuts import render

def login_ui(request):
    return render(request, 'login.html')

def chat_ui(request):
    return render(request, 'chat.html')

def register_ui(request):  #  New register UI view
    return render(request, 'register.html')
