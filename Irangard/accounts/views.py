import requests
import json
import uuid
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action, api_view, permission_classes
from .models import StagedPayments, SpecialUser
from django.contrib.auth import authenticate, login
from accounts.serializers.user_serializers import UserSerializer


class PayViewSet(GenericViewSet):

    permission_classes = [permissions.AllowAny]
    serializer_class = None
    
    # def get_serializer(self, *args, **kwargs):
    #     return None

    @action(detail=False, url_path='pay', methods=['POST','GET'], permission_classes=[permissions.AllowAny])
    def pay(self, request):



        order_id = str(uuid.uuid4())
        my_data = {
            "order_id": order_id,
            "amount": 50000,
            "name": f"{request.user.username}",
            "mail": f"{request.user.email}",
            "callback": "https://api.irangard.ml/accounts/pay/verify/"
        }

        my_headers = {"Content-Type": "application/json",
                      'X-API-KEY': '3394842f-7407-4598-8c48-499a15c8d0b7',
                      'X-SANDBOX': '0'}

        response = requests.post(url="https://api.idpay.ir/v1.1/payment", data=json.dumps(my_data),
                                 headers=my_headers)
        response.raise_for_status()
        print(response.status_code)
        try:
            obj = StagedPayments.objects.get(user=request.user)
            obj.transaction_id = json.loads(response.content)['id']
            obj.order_id = order_id
            obj.save()

        except StagedPayments.DoesNotExist:
            obj = StagedPayments.objects.create(transaction_id=json.loads(response.content)[
                'id'], order_id=order_id, user=request.user)
            obj.save()

        return Response(f"{json.loads(response.content)}", status=status.HTTP_200_OK)

    @action(detail=False, url_path='verify', methods=['POST','GET'], permission_classes=[permissions.AllowAny])
    def verify(self, request):

        username = 'emad12'
        password = 'emad1234'
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

        my_data = {
            "order_id": f'{request.user.staged_payments_info.order_id}',
            "id": f'{request.user.staged_payments_info.transaction_id}',

        }

        my_headers = {"Content-Type": "application/json",
                      'X-API-KEY': '3394842f-7407-4598-8c48-499a15c8d0b7',
                      'X-SANDBOX': '0'
                      }

        response = requests.post(url="https://api.idpay.ir/v1.1/payment/verify", data=json.dumps(my_data),
                                 headers=my_headers)
        response.raise_for_status()
        print(response.content, ' ', response.status_code)

        if(response.status_code == 200):
            sp_user = SpecialUser.objects.create(user = request.user)
            sp_user.save()
            st_payment = StagedPayments.objects.get(user = request.user)
            st_payment.delete()
            return Response(f"{json.loads(response.content)}", status=status.HTTP_200_OK)
