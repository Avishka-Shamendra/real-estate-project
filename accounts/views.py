from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User

def register(request):
    if(request.method=='POST'):
        # Get Form Values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Password match
        if(password!=password2):
            messages.error(request, "Passwords do not match")
            return redirect('register')
        elif(len(password)<3 or len(password)>20):
            messages.error(request, "Password mustr be more than 2 characters and less than 20 characters")
            return redirect('register')
        else:
            # Check username uniqueness
            if(User.objects.filter(username=username).exists()):
                messages.error(request, "Username already in use")
                return redirect('register')
            else:
                # Check email uniqueness
                if(User.objects.filter(email=email).exists()):
                    messages.error(request, "Email already in use")
                    return redirect('register')
                else:
                    # OK to register
                    user = User.objects.create_user(username=username,password=password, email=email,first_name=first_name,last_name=last_name)
                    # Option 1 Login after register
                    # auth.login(request, user)
                    # messages.success(request, "You are now registered and logged in")
                    # return redirect('index')
                    # Option 2 Redirect to reg with success msg
                    messages.success(request, "You are now registered successfully")
                    return redirect('login')

    # GET REQ
    return render(request,'accounts/register.html')

def login(request):
    if(request.method=='POST'):
        # Login user
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if(user is None):
            messages.error(request, "Username or Password Incorrect")
            return redirect('login')
        else:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('dashboard')

    # GET REQ
    return render(request,'accounts/login.html')

def logout(request):
    return redirect('index')

def dashboard(request):
    return render(request,'accounts/dashboard.html')