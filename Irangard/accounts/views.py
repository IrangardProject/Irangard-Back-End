from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from validate_email import validate_email
import random
from .serializers.user_serializers import UserSerializer
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from accounts.models import User, Verification
# Create your views here.


@api_view(http_method_names=['POST'])
def ActivationEmail(request):
    if request.method == 'POST':
        # remove_expired_tokens()
        user_email = request.data['email']
        user_username = request.data['username']

        if validate_email(user_email):
            rnd_tok = random.randrange(100000, 1000000)
            template = render_to_string('myemail/activation.html',
                                        {
                                            'username': user_username,
                                            'code': rnd_tok,
                                            'WEBSITE_URL': 'kooleposhti.tk',
                                        })

            email = EmailMessage('تایید حساب کاربری در ایرانگرد',
                                 template,
                                 settings.EMAIL_HOST_USER,
                                 [user_email]
                                 )

            email.content_subtype = "html"
            email.fail_silently = False
            email.send()

            try:
                # email resent
                verification_obj = Verification.objects.get(email=user_email)
                verification_obj.token = str(rnd_tok)
                verification_obj.save()

            except Verification.DoesNotExist:
                # email sent
                verification_obj = Verification.objects.create(
                    email=user_email,
                    token=str(rnd_tok))
                verification_obj.save()

            return Response(status=status.HTTP_200_OK, data='Email sent successfully')
            # return Response({"code": random_code}, status= status.HTTP_200_OK)

        else:
            return Response(f"'{user_email}' doesn't exist", status=status.HTTP_404_NOT_FOUND)


@api_view(http_method_names=['POST'])
def check_email(request):
    if request.method == 'POST':
        try:
            User.objects.get(email=request.data['email'])
            return Response(f"email '{request.data['email']}' already exists!",
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_200_OK, data='New Email')


@api_view(http_method_names=['POST'])
def check_username(request):
    if request.method == 'POST':
        try:
            User.objects.get(username=request.data['username'])
            return Response(f"username '{request.data['username']}' is already taken!",
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_200_OK, data='New Username')


@api_view(http_method_names=['POST'])
def activate(request):
    if request.method == 'POST':
        try:
            User.objects.get(email=request.data['email'])
            return Response(f"email '{request.data['email']}' already exists!",
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:

            try:
                User.objects.get(username=request.data['username'])
                return Response(f"username '{request.data['username']}' is already taken!",
                                status=status.HTTP_400_BAD_REQUEST)

            except User.DoesNotExist:
                return ActivationEmail(request._request)


@api_view(http_method_names=['POST'])
def set_password(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.data['username'])
            if(request.data['password'] == request.data['re_password']):
                updated_user = {"username": user.username,
                                "email": user.email,
                                "password":request.data['password']}
                user_serializer = UserSerializer(user, data=updated_user)
                if(user_serializer.is_valid()):
                    user_serializer.save()                    
                    return Response(user_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(user_serializer.errors)
            else:
                return Response(f"password and re-password are not same",
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(f"user with username '{request.data['username']}' doesn't exist",
                            status=status.HTTP_400_BAD_REQUEST)
