from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages, auth
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
import pywhatkit as kit
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Create your views here.
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    def post(self, request):
        # messages.success(request, "Success message")
        #GET data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        context = {
            'fieldValues': request.POST
        }
        #Validate
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password is too Short")
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
                activate_url = "http://"+domain+link
                email_subject = "Activate Your Account"
                email_body = "Hi "+user.username+ " Please use this link to verify your account\n" + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    "noreply@example.com",
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'User Created Successfully!!')
                return render(request, 'authentication/register.html')
        #create user account
        
   
        return render(request, 'authentication/register.html')

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = urlsafe_base64_decode(uidb64).decode('utf-8')
            # val = id.decode('utf-8')
            # print()
            user = User.objects.get(pk=id)
            if not token_generator.check_token(user, token):
                return redirect('login'+'?messages='+'User Already Activated')
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'User Account activated Successfully!!')
            return redirect('login')
        except Exception as e:
            # messages.error(request, "The error is "+id)
            pass
        return redirect('login')
    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "User Logged in Successfully!!")
                    phone_number = "+254719189576"
                    message = "Hello from Python! This is an instant WhatsApp message."
                    # Send the message instantly
                    # kit.sendwhatmsg_instantly(phone_number, message)
                    # kit.sendwhatmsg_instantly(phone_number, message)
                    return redirect('expenses')
                messages.error(request, "Account Not activated, Please Check your Email")
                return render(request, 'authentication/login.html')
            messages.error(request, "Invalid Credentials")
            return render(request, 'authentication/login.html')
        messages.error(request, "Please fill all Fields")
        return render(request, 'authentication/login.html')

class UsernameValidationView(View):
    def post(self, request):
        data= json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error' : 'username should only contain alphanumerical!'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error' : 'username exists, enter another username'}, status=409)
        return JsonResponse({'username_valid': True})
    
class EmailValidationView(View):
    def post(self, request):
        data= json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error' : 'Email is Invalid!'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error' : 'email exists, enter another email'}, status=409)
        return JsonResponse({'email_valid': True})
    

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "User Logged out Successfully!!")
        return redirect('login')
class RequestPasswordResetEmail(View):
    def get(self, request):
        # messages.success(request, "User Logged out Successfully!!")
        return render(request, 'authentication/reset-password.html')
    def post(self, request):
        email = request.POST['email']
        context = {
            'values': request.POST
        }
        if not validate_email(email):
            messages.error(request, "Please Enter Valiad Email!!")
            return render(request, 'authentication/reset-password.html', context)
        user = User.objects.filter(email=email)
        if user.exists():
            uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64': uidb64, 'token': PasswordResetTokenGenerator().make_token(user[0])})
            activate_url = "http://"+domain+link
            email_subject = "Reset Your Account Password"
            email_body = "Hi "+user[0].username+ " Please use this link to reset your account password\n" + activate_url
            email = EmailMessage(
                email_subject,
                email_body,
                "noreply@example.com",
                [email],
            )
            email.send(fail_silently=False)
        messages.success(request, "We have sent you an email!!")
        
        messages.success(request, "Reset Email Sent Successfully!!")
        return render(request, 'authentication/reset-password.html')