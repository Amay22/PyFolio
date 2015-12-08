'''Login.views Supports all the user authentication and login and registering process'''
from django.shortcuts import render, redirect
# Takes care of checking if the user is logged in or not
from django.contrib.auth.decorators import login_required
# Takes care of all the basic login, authenticizing and login process for tokenization
from django.contrib.auth import login, logout, authenticate
# The in-built django user module will take care of all the user related database functionality
from django.contrib.auth.models import User
# User of this App
from StockFolio.models import StockFolioUser

@login_required
def index():
  '''Redirects right to the portfolio page that that serves as a user dashboard'''
  return redirect('portfolio')

def login_user(request):
  '''Form support for Login'''
  if request.method == "POST":
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')

    authenticated = authenticate(username=email, password=password)

    # Valid username and password
    if authenticated is not None and authenticated.is_active:
      login(request, authenticated)
      return redirect('portfolio')
    # Incorrect username or password
    else:
      return render(request, 'LoginFolio/login.html', {'errors': ['Invalid Username and/or Password']})

  else:
    # Displacy Login Form
    return render(request, 'LoginFolio/login.html')

def register_user(request):
  '''Form support for User Registration Process'''
  if request.method == "POST":
    # Get POST params from request
    f_name = request.POST.get('first_name', '')
    l_name = request.POST.get('last_name', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    confirm_password = request.POST.get('password_confirmation', '')

    errors = []
    # Check if the user already exists
    try:
      User.objects.get(username=email)
      errors.append('A user by that username already exists')
    except User.DoesNotExist:
      pass

    # Input Field checks
    if len(password) < 3:
      errors.append('Enter a valid password that is more than 3 characters')
    if password != confirm_password:
      errors.append('Password and Confirm Password don\'t match')
    if len(errors) > 0:
      return render(request, 'LoginFolio/register.html', {'errors' : errors})

    # Create a User and redirect to login
    user = User.objects.create_user(email, password=password)
    StockFolioUser.objects.create(user=user, first_name=f_name, last_name=l_name)
    return render(request, 'LoginFolio/login.html')
  else:
    # Display registration form
    return render(request, 'LoginFolio/register.html')

def logout_user(request):
  '''Logouts the currently signed in user and redirects to login'''
  logout(request)
  return redirect('LoginFolio/login.html')

def home(request):
  '''Redirects to the Home page'''
  return render(request, 'home.html')

def about(request):
  '''Redirects to the Home page'''
  return render(request, 'about.html')

def team(request):
  '''Redirects to the Team page'''
  return render(request, 'team.html')

