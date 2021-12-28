from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from .forms import CreateUserForm, UserForm
from .models import User
from main.models import Room, Topic
from .token import generate_token

# Create your views here.

# Send email
def send_email(user, request):
        current_site = get_current_site(request)
        email_subject = 'Activate your account.'
        email_body = render_to_string('activate_account.html',{
            'user':user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user]

        email = EmailMessage(subject=email_subject, body=email_body,  from_email=from_email, to=recipient_list)

        return email.send(fail_silently = False)
  
    
# Register User
def registerUser(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save() 
            # send account verification email
            send_email(user, request)
            messages.success(request, f"We have sent you an email, please confirm your email address to complete registration!")
            return redirect('login')
        else:
            messages.error(request, "Something went wrong. Please try again!")

    context = {'form':form}
    return render(request, 'register.html', context)


# Login User
def loginUser(request):

    # checking if user is authenticated
    if request.user.is_authenticated:
        return redirect('home')

    # getting next value if exist
    next = ""
    if request.GET:  
        next = request.GET['next']

    # getting user data
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # authenticating user
        user = authenticate(request, email=email, password=password)
        # login user
        if user is not None:
            login(request, user)
            messages.success(request, f'Logged in successful as {user.username}!')
            if next == "":
                return redirect('home')
            else:
                return redirect(next)
        else:
            messages.error(request, 'Incorrect email or password!')

    return render(request, 'login.html')


# Logout User
def logoutUser(request):
    logout(request)
    return redirect('home')


# User Profile
def profileUser(request, pk):
    user = User.objects.get(id=pk) # getting user 
    rooms = user.room_set.all()    # getting rooms

    # pagination 
    paginator = Paginator(rooms, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    room_messages = user.message_set.all() # getting room messages
    topics_all = Topic.objects.all() # getting topics
    context = {'user':user, 'rooms':rooms, 'page_obj':page_obj, 'room_messages':room_messages, 'topics_all':topics_all}
    return render(request, 'user_profile.html', context)


# Update User Account
@login_required(login_url=login)
def updateUser(request):
    form = UserForm(instance=request.user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_user', pk=request.user.id)

    context = {'form':form}
    return render(request, 'user_account.html', context)    


# Activate Account
def activateUser(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if user exist and token is valid
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been verified!')
        return redirect('home')
    else:
        messages.warning(request, 'Activation link is invalid or expired, please enter your email again!')      
        return redirect('generate_link')


# Generate Link
def generateLink(request):
    if request.method == 'POST':   
        # getting email   
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        # sending email to user 
        if user is not None:
            send_email(user, request)   
            messages.success(request, f"We have sent you a link to your given email.")
            return redirect('login')
        else:
            messages.warning(request, f"Account does not exist, please signup!")
            return redirect('register')

    return render(request, 'generate_link.html')


