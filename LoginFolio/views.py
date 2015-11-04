"""Login.views Supports all the user authentication and login and registering process"""
from django.shortcuts import render, redirect
# Takes care of checking if the user is logged in or not
from django.contrib.auth.decorators import login_required
# Takes care of all the basic login, authenticizing and login process for tokenization
from django.contrib.auth import login, logout, authenticate
# The in-built django user module will take care of all the user related database functionality
from django.contrib.auth.models import User

@login_required
def index():
  """Redirects right to the portfolio page that that serves as a user dashboard"""
  return redirect('portfolio')

def login_user(request):
  """Form support for Login"""
  if request.method == "POST":
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    errors = []

    if username is None or not username:
      errors.append('Invalid Username')
    if password is None or not password:
      errors.append('Invalid Password')
    if len(errors) > 0:
      return render(request, 'login/login.html', {'errors' : errors})

    authenticated = authenticate(username=username, password=password)

    # Valid username and password
    if authenticated is not None and authenticated.is_active:
      login(request, authenticated)
      return redirect('portfolio')
    # Incorrect username or password
    else:
      return render(request, 'login/login.html', {'errors': ['Invalid Username and/or Password']})

  else:
    # Displacy Login Form
    return render(request, 'login/login.html')

def register_user(request):
  """Form support for User Registration Process"""
  if request.method == "POST":
    # Get POST params from request
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    confirm_password = request.POST.get('confirm-pass', '')

    errors = []
    # Check if the user already exists
    try:
      User.objects.get(username=username)
      errors.append('A user by that username already exists')
    except User.DoesNotExist:
      pass
    # Input Field checks
    if len(username) < 3:
      errors.append('Enter a valid Username that is more than 3 characters')
    if len(password) < 3:
      errors.append('Enter a valid password that is more than 3 characters')
    if password != confirm_password:
      errors.append('Password and Confirm Password don\'t match')
    if len(errors) > 0:
      return render(request, 'login/register.html', {'errors' : errors})

    return render(request, 'login/login.html')
  else:
    # Display registration form
    return render(request, 'login/register.html')

def logout_user(request):
  """Logouts the currently signed in user and redirects to login"""
  logout(request)
  return redirect('login')
