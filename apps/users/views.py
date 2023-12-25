from django.shortcuts import render

# Create your views here.



from django.contrib.auth import logout

def home(request):
    return render(request, "home.html")

def landing(request):
    return render(request, "landing-page.html")

def logout_view(request):
    logout(request)
    return render(request, "/")
