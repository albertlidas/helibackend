from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from landing.models import Email


def home_page(request):
    return render(request, 'index.html')


def login_page(request):
    return render(request, 'login.html')


def signup_page(request):
    return render(request, 'signup.html')


def manager_page(request):
    return render(request, 'manager.html')


class SendMail(APIView):
    def post(self, request):
        data = request.data
        try:
            message = 'E-mail: {} \n\nMessage: {}'.format(data['email'], data['text'])
            send_mail(data['text'], message, data['email'],
                      [settings.EMAIL_HOST_USER], fail_silently=False)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SaveEmail(APIView):
    def post(self, request):
        data = request.data
        if data['email']:
            email_object = Email(email=data['email'])
            email_object.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
