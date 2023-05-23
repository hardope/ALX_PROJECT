from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse("authenticate"))
    return HttpResponse(f"Hello, {request.user}.... You're at the main index.")

def authenticate_view(request):
    if request.method == "POST":

        if request.POST.get("action") == "login":

            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "message": "Invalid username or password"})
        elif request.POST.get("action") == "sign_up":

            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            print(f"Username: {username}, Email: {email}, Password: {password}, Confirm Password: {confirm_password}")
            if password != confirm_password:
                return JsonResponse({"success": False, "message": "Password and Confirm Password do not match"})
            if User.objects.filter(username=username).exists():
                return JsonResponse({"success": False, "message": "Username already exists"})
            if User.objects.filter(email=email).exists():
                return JsonResponse({"success": False, "message": "Email already exists"})
            return JsonResponse({"success": True})

        elif request.POST.get("action") == "verify_otp":

            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            otp = request.POST.get("otp")
            if otp != "1234":
                return JsonResponse({"success": False, "message": "Invalid OTP"})
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            user = User.objects.get(username=request.POST.get("username"))
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            login(request, user)

            return JsonResponse({"success": True})

    return render(request, "authenticate.html")