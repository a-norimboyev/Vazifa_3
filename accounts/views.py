from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm, UserLoginForm

# Create your views here.

def register_view(request):
    if request.user.is_authenticated:
        return redirect("blog:home")
        
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}! Ro'yxatdan muvaffaqiyatli o'tdingiz.")
            return redirect("blog:home")
    else:
        form = RegisterForm()
        
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("blog:home")
        
    next_url = request.GET.get("next") or request.POST.get("next") or "blog:home"
    
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Salom, {user.username}! Tizimga muvaffaqiyatli kirdingiz.")
            if next_url and next_url != "None":
                return redirect(next_url)
            return redirect("blog:home")
    else:
        form = UserLoginForm()
        
    return render(request, "accounts/login.html", {"form": form, "next": next_url})


def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz.")
    return redirect("blog:home")
