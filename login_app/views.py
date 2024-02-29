from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from . import forms
from .models import User
from django.contrib import messages
from .forms import UserForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


# View to register form
def register(request):
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to your home page
    else:
        form = UserForm()
    return render(request, 'registration/register.html', {'form': form})


# View to login user
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        messages.success(request, "You're logged in", extra_tags='success')
        return redirect('Home')

    if request.method == 'POST':
        email = request.POST.get('email')
        if email is not None:
            email = email.lower()  # Convert to lowercase
        else:
            messages.error(request, 'Email is required', extra_tags='error')

        password = request.POST.get('password')

        try:
            # Perform a case-insensitive lookup
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist', extra_tags='error')
            return redirect('loginpage')

        # Check if the user exists and if the password is correct

        if user and user.check_password(password):
            if user.is_verified:
                messages.success(request, "You're logged in", extra_tags='success')
                login(request, user)
            else:
                messages.error(request, "Verify your account first", extra_tags='error')
                return redirect('loginpage')
            return redirect('Home')
        else:
            messages.error(request, 'Email or password does not exist', extra_tags='error')

    context = {'page': page}
    return render(request, 'registration/login_2.html', context)


# View to logout user
def logoutUser(request):
    logout(request)
    messages.success(request, "You've been logged out", extra_tags='success')
    return redirect('/')


# View to register user with email validation
def registerPage(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email'].lower()
            user.set_password(form.cleaned_data['password'])
            user.is_verified = False
            user.save()

            # Send verification email
            subject = 'Verify your account'
            user_id_b64 = urlsafe_base64_encode(user.pk.to_bytes(4, byteorder='big'))
            token = default_token_generator.make_token(user)
            verification_url = reverse('verify_email', kwargs={'user_id': user_id_b64, 'token': token})
            message = f'Click the link to verify your account: <a href="http://127.0.0.1:8000{verification_url}">http://127.0.0.1:8000{verification_url}</a>'
            from_email = 'your@example.com'  # Update with your email
            to_email = [user.email]
            send_mail(subject=subject, message="Hi :)", from_email=from_email, recipient_list=to_email,
                      html_message=message)

            messages.success(request, 'Account created. Check your email to verify your account.')
            return redirect('Home')
        else:
            messages.error(request, 'An error occurred :o')

    return render(request, 'registration/login_2.html', {'form': form})


# verifying email
def verify_email(request, user_id, token):
    print("Received user_id:", user_id)
    print("Received token:", token)

    try:
        user_id_decoded = int.from_bytes(urlsafe_base64_decode(user_id), byteorder='big')
        print("Decoded user_id:", user_id_decoded)

        user = User.objects.get(pk=user_id_decoded)
        print("User found:", user)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        print("Error:", e)
        user = None

    print("Final user:", user)

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, 'Email verified successfully. You can now log in.')
    else:
        messages.error(request, 'Invalid verification link.')

    return redirect('loginpage')
