import requests
import json
import uuid
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action, api_view, permission_classes
from .models import StagedPayments, SpecialUser, User
from django.contrib.auth import authenticate, login
from accounts.serializers.payment_serializers import VerifiedPaymentSerializer
from django.template.loader import render_to_string


class PayViewSet(GenericViewSet):

    permission_classes = [permissions.AllowAny]
    serializer_class = VerifiedPaymentSerializer

    # def get_serializer(self, *args, **kwargs):
    #     return None

    @action(detail=False, url_path='pay', methods=['POST', 'GET'], permission_classes=[permissions.AllowAny])
    def pay(self, request):

        if(hasattr(request.user, 'special_users') and request.user.special_users is not None):
            return Response(f"user {request.user.username} is already a special user", status=status.HTTP_400_BAD_REQUEST)
        order_id = str(uuid.uuid4())
        my_data = {
            "order_id": order_id,
            "amount": 10000,
            "name": f"{request.user.username}",
            "mail": f"{request.user.email}",
            "callback": "https://api.quilco.ir/accounts/pay/verify/"
        }

        my_headers = {"Content-Type": "application/json",
                      'X-API-KEY': '6f304859-1d0c-461a-b5f3-1d7bd9d3fd5b',
                      'X-SANDBOX': '1'}

        
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
                'id'], order_id=order_id, user=request.user, amount=10000)
            obj.save()
        except:
            return Response(f"bad request", status=status.HTTP_400_BAD_REQUEST)

        return Response(json.loads(response.content), status=status.HTTP_200_OK)

    @action(detail=False, url_path='verify', methods=['POST', 'GET'], permission_classes=[permissions.AllowAny])
    def verify(self, request):

        try:
            my_data = {
                "order_id": request.data['order_id'],
                "id": request.data['id'],

            }

            my_headers = {"Content-Type": "application/json",
                          'X-API-KEY': '6f304859-1d0c-461a-b5f3-1d7bd9d3fd5b',
                          'X-SANDBOX': '1'
                          }

            response = requests.post(url="https://api.idpay.ir/v1.1/payment/verify", data=json.dumps(my_data),
                                     headers=my_headers)
            response.raise_for_status()
            #print(response.content, ' ', response.status_code)

            if(response.status_code == 200):

                try:
                    staged_payments_user = StagedPayments.objects.get(
                        transaction_id=request.data['id']).user
                    user = User.objects.get(username=staged_payments_user.username)
                    user.is_special = True
                    user.save()
                    sp_user = SpecialUser.objects.create(user=user)
                    sp_user.save()
                    st_payment = StagedPayments.objects.get(user=user)
                    st_payment.delete()
                    verified_payment_serializer = VerifiedPaymentSerializer(data = json.loads(response.content)) 
                    verified_payment_serializer.is_valid(raise_exception=True)
                    template = render_to_string('success_payment.html',
                            {
                                'username': user.username,
                                'code': '123',
                                'WEBSITE_URL': 'kooleposhti.tk',
                            })
                    return HttpResponse(template)
                    #return Response(verified_payment_serializer.data, status=status.HTTP_200_OK)
                except StagedPayments.DoesNotExist:
                    return Response(f"there is no corresponding payment to be verified", status=status.HTTP_400_BAD_REQUEST)
                except Exception as error:
                    print(error)
                    return Response(f"user {user.username} is already a special user", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(f"transaction is not verified", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except:
            return Response(f"order id is required", status=status.HTTP_400_BAD_REQUEST)


class WalletViewSet(GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifiedPaymentSerializer

    @action(detail=False, url_path='increase', methods=['POST', 'GET'], permission_classes=[permissions.AllowAny])
    def increase_wallet_credit(self, request):
        amount = request.data['amount']
        order_id = str(uuid.uuid4())
        my_data = {
            "order_id": order_id,
            "amount": amount,
            "name": f"{request.user.username}",
            "mail": f"{request.user.email}",
            "callback": "https://api.quilco.ir/accounts/wallet/increase/verify/"
        }

        my_headers = {"Content-Type": "application/json",
                      'X-API-KEY': '6f304859-1d0c-461a-b5f3-1d7bd9d3fd5b',
                      'X-SANDBOX': '1'}

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
                'id'], order_id=order_id, user=request.user, amount=amount)
            obj.save()
        except:
            return Response(f"bad request", status=status.HTTP_400_BAD_REQUEST)
        return Response(json.loads(response.content), status=status.HTTP_200_OK)

    @action(detail=False, url_path='increase/verify', methods=['POST', 'GET'], permission_classes=[permissions.AllowAny])
    def verify_wallet_increment(self, request):
        try:
            my_data = {
                "order_id": request.data['order_id'],
                "id": request.data['id'],

            }
            my_headers = {"Content-Type": "application/json",
                          'X-API-KEY': '6f304859-1d0c-461a-b5f3-1d7bd9d3fd5b',
                          'X-SANDBOX': '1'
                          }
            response = requests.post(url="https://api.idpay.ir/v1.1/payment/verify", data=json.dumps(my_data),
                                     headers=my_headers)
            response.raise_for_status()
            if(response.status_code == 200):
                try:
                    this_st_payment = StagedPayments.objects.get(transaction_id=request.data['id'])
                    staged_payments_user = this_st_payment.user
                    user = User.objects.get(username=staged_payments_user.username)
                    user.increase_wallet_credit(this_st_payment.amount)
                    user.save()
                    amount = this_st_payment.amount
                    all_st_payment = StagedPayments.objects.get(user=user)
                    all_st_payment.delete()
                    verified_payment_serializer = VerifiedPaymentSerializer(data = json.loads(response.content))
                    verified_payment_serializer.is_valid(raise_exception=True)
                    template = render_to_string('success_wallet_charge.html',
                            {
                                'username': user.username,
                                'code': '123',
                                'WEBSITE_URL': 'kooleposhti.tk',
                                'amount' : amount,
                            })
                    return HttpResponse(template)
                except StagedPayments.DoesNotExist:
                    return Response(f"there is no corresponding payment to be verified", status=status.HTTP_400_BAD_REQUEST)
                except Exception as error:
                    print(error)
                    return Response(f"bad request", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(f"transaction is not verified", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except:
            return Response(f"order id is required", status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, url_path='decrease', methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def decrease_wallet_credit(self, request):
        if not request.data.get('amount'):
            return Response(f"you should specify amount", status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        amount = request.data.get('amount')
        try:
            user.decrease_wallet_credit(amount)
        except Exception :
            return Response({'error' : 'not enough credit'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'credit' : user.wallet_credit}, status=status.HTTP_200_OK)

