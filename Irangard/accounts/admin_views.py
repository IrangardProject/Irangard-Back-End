import json
from collections import defaultdict
from django.shortcuts import render
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg, Count, Min, Sum

from tours.models import Tour
from .models import User, SpecialUser
from .serializers.user_serializers import UserProfileSerializer, UserBasicInfoSerializer, UserSerializer
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.test import APIClient
from . permissions import IsAdmin
from accounts.serializers.serializers import *
from experience.serializers import *
from places.serializers import *
from places.models import *
from experience.models import *
from accounts.models import *
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class AdminViewSet(GenericViewSet):
    queryset = User.objects.filter(is_admin=True)

    # @action(detail=False, url_path='upgrade-user',  methods=['POST'], permission_classes=[IsAdmin])
    # def UpgradeUser(self, request):
    #     user = User.objects.get(username = request.user.username)
    #     special_user = SpecialUser.objects.create(user = user)
    #     special_user.save()
    #     return Response(f"user with username {request.user.username} upgraded to special user successfully",status = HTTP_200_OK)

    @action(detail=False, url_path='add-admin', methods=['POST'], permission_classes=[permissions.AllowAny])
    def addAdmin(self, request):
        try:
            user = User.objects.get(username=request.user.username)
            user.is_admin = True
            user.save()
            return Response(f'user with username {request.user.username} added as admin', status=status.HTTP_200_OK)
        except:
            return Response(f'unAuthenticated user', status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, url_path='remove-specialuser', methods=['POST'], permission_classes=[IsAdmin])
    def removeSpecialUser(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            sp_user = SpecialUser.objects.get(user=user)
            sp_user.delete()
            user.is_special = False
            user.save()
            return Response(f'special user with username {user.username} deleted', status=status.HTTP_200_OK)
        except SpecialUser.DoesNotExist:
            return Response(f'special user with username {user.username} doesn not exist', status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path='remove-user', methods=['POST'], permission_classes=[IsAdmin])
    def removeUser(self, request):
        try:
            if('username' not in request.data):
                return Response(f'no usernmae is provieded', status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(username=request.data['username'])
            if(user.is_admin):
                return Response(f'admin user can not be removed', status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
            if(user.is_special):
                return Response(f'special user can not be removed', status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
            user.delete()
            return Response(f'user with username {user.username} deleted', status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(f'user with username {user.username} doesn not exist', status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path='add-user', methods=['POST'], permission_classes=[IsAdmin])
    def addUser(self, request):

        if('username' not in request.data):
            return Response(f'no usernmae is provieded', status=status.HTTP_400_BAD_REQUEST)
        if('email' not in request.data):
            return Response(f'no email is provieded', status=status.HTTP_400_BAD_REQUEST)
        if('password' not in request.data):
            return Response(f'no password is provieded', status=status.HTTP_400_BAD_REQUEST)
        if(request.data['re_password'] != request.data['password']):
            return Response(f'password and re_password are not same', status=status.HTTP_400_BAD_REQUEST)

        client = APIClient()
        url = reverse('accounts:accounts-auth-check-username')
        response = client.post(url, json.dumps(
            {"username": request.data['username']}), content_type='application/json')
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            return Response(f'username already exists', status=status.HTTP_400_BAD_REQUEST)

        url = reverse('accounts:accounts-auth-check-email')
        response = client.post(url, json.dumps(
            {"email": request.data['email']}), content_type='application/json')
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            return Response(f'email already exists', status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=request.data['username'], email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        serializer = UserBasicInfoSerializer(data=request.data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, url_path='basic-statistics', methods=['GET'], permission_classes=[IsAdmin])
    def basicStatistics(self, request):
        statistics = defaultdict(int)

        statistics['users_no'] = len(User.objects.all())
        statistics['special-users_no'] = len(SpecialUser.objects.all())
        statistics['places_no'] = len(Place.objects.all())
        statistics['experiences_no'] = len(Experience.objects.all())
        statistics['top_10_liked_experiences'] = ExperienceSerializer(
            Experience.objects.all().order_by('-like_number')[:10], many=True).data
        statistics['tour_no'] = len(Tour.objects.all())
        statistics['users_revenue'] = SpecialUser.objects.aggregate(Sum('total_revenue'))
        statistics['top_10_person_with_most_follower'] = UserSerializer(
            User.objects.all().order_by('follower_number')[:10], many=True).data
        return Response(statistics, status=status.HTTP_200_OK)

    @action(detail=False, url_path='daily-statistics', methods=['POST'], permission_classes=[IsAdmin])
    def dailyStatistics(self, request):
        statistics = defaultdict(int)
        start_date = datetime.strptime(
            request.data['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(
            request.data['end_date'], "%Y-%m-%d").date()
        delta = timedelta(days=1)

        try:
            # start find count of added user per day in range of strart_date and end-date
            added_daily_user = dict()
            start = start_date
            while start <= end_date:
                print(start)
                try:
                    queryset = User.objects.filter(
                        date_joined__day=start.day)
                    queryset = queryset.filter(
                        date_joined__month=start.month)
                    queryset = queryset.filter(
                        date_joined__year=start.year)
                    if(len(queryset) > 0):
                        added_daily_user[f'{start}'] = len(queryset)
                except Exception as error:
                    print(error)

                start += delta

            statistics['added_daily_user'] = added_daily_user

            # finish find count of added user per day in range of strart_date and end-date
            
            #start find count of added special user per day in range of strart_date and end-date
            
            added_daily_special_user = dict()
            start = start_date
            while start <= end_date:
                print(start)
                try:
                    queryset = SpecialUser.objects.filter(
                        user__date_joined__day=start.day)
                    queryset = queryset.filter(
                        user__date_joined__month=start.month)
                    queryset = queryset.filter(
                        user__date_joined__year=start.year)
                    if(len(queryset) > 0):
                        added_daily_special_user[f'{start}'] = len(queryset)
                except Exception as error:
                    print(error)

                start += delta

            statistics['added_daily_special_user'] = added_daily_special_user
            
            # find count of added experience per day in range of strart_date and end-date
            
            added_daily_experience = dict()
            start = start_date
            while start <= end_date:
                try:
                    queryset = Experience.objects.filter(date_created__day=start.day)
                    queryset = queryset.filter(date_created__month=start.month)
                    queryset = queryset.filter(date_created__year=start.year)
                    if(len(queryset) > 0):
                        added_daily_experience[f'{start}'] = len(queryset)
                except Exception as error:
                    print(error)
                    
                start += delta
                
            statistics['added_daily_experience'] = added_daily_experience
            
            
            # find count of added places per day in range of strart_date and end-date
            
            added_daily_places = dict()
            start = start_date
            while start <= end_date:
                try:
                    queryset = Place.objects.filter(date_created__day=start.day)
                    queryset = queryset.filter(date_created__month=start.month)
                    queryset = queryset.filter(date_created__year=start.year)
                    if(len(queryset) > 0):
                        added_daily_places[f'{start}'] = len(queryset)
                except Exception as error:
                    print(error)
                    
                start += delta
                
            statistics['added_daily_place'] = added_daily_places
            
            # find count of added tours per day in range of strart_date and end-date
            
            added_daily_tours = dict()
            start = start_date
            while start <= end_date:
                try:
                    queryset = Tour.objects.filter(date_created__day=start.day)
                    queryset = queryset.filter(date_created__month=start.month)
                    queryset = queryset.filter(date_created__year=start.year)
                    if(len(queryset) > 0):
                        added_daily_tours[f'{start}'] = len(queryset)
                except Exception as error:
                    print(error)
                    
                start += delta
                
            statistics['added_daily_tour'] = added_daily_tours
            
            #filter find count of added special users per day in range of strart_date and end-date
            

        except Exception as error:
            return Response(f'bad request', status=status.HTTP_400_BAD_REQUEST)

        return Response(statistics, status=status.HTTP_200_OK)

    @action(detail=False, url_path='weekly-statistics', methods=['POST'], permission_classes=[IsAdmin])
    def weeklyStatistics(self, request):
        statistics = defaultdict(int)
        start_date = datetime.strptime(
            request.data['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(
            request.data['end_date'], "%Y-%m-%d").date()
        delta = timedelta(days=6)

        try:
            # start find count of added user per day in range of strart_date and end-date
            added_weekly_user = dict()
            start = start_date
            while start <= end_date:
                print(start)
                try:
                    queryset = User.objects.filter(
                        date_joined__day__gte=start.day)
                    if(not ((start.day >= 24 and start.month in [7,8,9,10,11,12]) or (start.day >=25 and start.month in [1,2,3,4,5,6]))):
                        queryset = queryset.filter(date_joined__day__lte=(start+delta).day)
                    queryset = queryset.filter(
                        date_joined__month=start.month)
                    queryset = queryset.filter(
                        date_joined__year=start.year)
                    if(len(queryset) > 0):
                        added_weekly_user[f'{start} - {start+delta}'] = len(queryset)
                except Exception as error:
                    print(error)

                start += delta

            statistics['added_weekly_user'] = added_weekly_user

            # finish find count of added user per day in range of strart_date and end-date
            
            #start find count of added special user per day in range of strart_date and end-date
            
            added_weekly_special_user = dict()
            start = start_date
            while start <= end_date:
                print(start)
                try:
                    queryset = SpecialUser.objects.filter(
                        user__date_joined__day__gte=start.day)
                    if(not ((start.day >= 24 and start.month in [7,8,9,10,11,12]) or (start.day >=25 and start.month in [1,2,3,4,5,6]))):
                        queryset = queryset.filter(user__date_joined__day__lte=(start+delta).day)
                    queryset = queryset.filter(
                        user__date_joined__month=start.month)
                    queryset = queryset.filter(
                        user__date_joined__year=start.year)
                    if(len(queryset) > 0):
                        added_weekly_special_user[f'{start} - {start+delta}'] = len(queryset)
                except Exception as error:
                    print(error)

                start += delta

            statistics['added_weekly_special_user'] = added_weekly_special_user
            
            #filter find count of added special users per day in range of strart_date and end-date
            
            
            #start find count of added experience per week in range of strart_date and end-date
            
            added_weekly_experience = dict()
            start = start_date
            while start <= end_date:
                print(start)
                try:
                    queryset = Experience.objects.filter(
                        date_created__day__gte=start.day)
                    if(not ((start.day >= 24 and start.month in [7,8,9,10,11,12]) or (start.day >=25 and start.month in [1,2,3,4,5,6]))):
                        queryset = queryset.filter(date_created__day__lte=(start+delta).day)
                    queryset = queryset.filter(
                        date_created__month=start.month)
                    queryset = queryset.filter(
                        date_created__year=start.year)
                    if(len(queryset) > 0):
                        added_weekly_experience[f'{start} - {start+delta}'] = len(queryset)
                except Exception as error:
                    print(error)

                start += delta

            statistics['added_weekly_experience'] = added_weekly_experience
            
            
            #start find count of added tours per week in range of strart_date and end-date
            
            added_weekly_tours = dict()
            start = start_date
            while start <= end_date:
                print(start)
                try:
                    queryset = Tour.objects.filter(
                        date_created__day__gte=start.day)
                    if(not ((start.day >= 24 and start.month in [7,8,9,10,11,12]) or (start.day >=25 and start.month in [1,2,3,4,5,6]))):
                        queryset = queryset.filter(date_created__day__lte=(start+delta).day)
                    queryset = queryset.filter(
                        date_created__month=start.month)
                    queryset = queryset.filter(
                        date_created__year=start.year)
                    if(len(queryset) > 0):
                        added_weekly_tours[f'{start} - {start+delta}'] = len(queryset)
                except Exception as error:
                    print(error)

                start += delta

            statistics['added_weekly_tour'] = added_weekly_tours
            
            
            #start find count of added places per week in range of strart_date and end-date
            
            added_weekly_places = dict()
            start = start_date
            while start <= end_date:
                print(start)
                try:
                    queryset = Place.objects.filter(
                        date_created__day__gte=start.day)
                    if(not ((start.day >= 24 and start.month in [7,8,9,10,11,12]) or (start.day >=25 and start.month in [1,2,3,4,5,6]))):
                        queryset = queryset.filter(date_created__day__lte=(start+delta).day)
                    queryset = queryset.filter(
                        date_created__month=start.month)
                    queryset = queryset.filter(
                        date_created__year=start.year)
                    if(len(queryset) > 0):
                        added_weekly_places[f'{start} - {start+delta}'] = len(queryset)
                except Exception as error:
                    print(error)

                start += delta

            statistics['added_weekly_place'] = added_weekly_places
            

        except Exception as error:
            return Response(f'bad request', status=status.HTTP_400_BAD_REQUEST)

        return Response(statistics, status=status.HTTP_200_OK)

    @action(detail=False, url_path='monthly-statistics', methods=['POST'], permission_classes=[IsAdmin])
    def monthlyStatistics(self, request):
        statistics = defaultdict(int)
        start_date = datetime.strptime(
            request.data['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(
            request.data['end_date'], "%Y-%m-%d").date()
        delta = relativedelta(months=1)

        try:
            # start find count of added user per day in range of strart_date and end-date
            added_monthly_user = dict()
            start = start_date
            while start <= end_date:
                print(start)
                try:
                    queryset = User.objects.filter(
                        date_joined__month=start.month)
                    queryset = queryset.filter(
                        date_joined__year=start.year)
                    if(len(queryset) > 0):
                        added_monthly_user[f'{start.strftime("%B")}'] = len(queryset)
                except Exception as error:
                    print(error)

                start += delta

            statistics['added_monthly_user'] = added_monthly_user

            # finish find count of added user per day in range of strart_date and end-date
            
            #start find count of added special user per day in range of strart_date and end-date
            
            added_monthly_special_user = dict()
            start = start_date
            while start <= end_date:
                print(start)
                try:
                    queryset = SpecialUser.objects.filter(
                        user__date_joined__month=start.month)
                    queryset = queryset.filter(
                        user__date_joined__year=start.year)
                    if(len(queryset) > 0):
                        added_monthly_special_user[f'{start.strftime("%B")}'] = len(queryset)
                except Exception as error:
                    print(error)

                start += delta

            statistics['added_monthly_special_user'] = added_monthly_special_user
            
            #filter find count of added special users per day in range of strart_date and end-date
            
            # start find count of added experience per month in range of strart_date and end-date
            added_monthly_experience = dict()
            start = start_date
            while start <= end_date:
                print(start)
                try:
                    queryset = Experience.objects.filter(
                        date_created__month=start.month)
                    queryset = queryset.filter(
                        date_created__year=start.year)
                    if(len(queryset) > 0):
                        added_monthly_experience[f'{start.strftime("%B")}'] = len(queryset)
                except Exception as error:
                    print(error)

                start += delta

            statistics['added_monthly_experience'] = added_monthly_experience

            # finish find count of added experience per month in range of strart_date and end-date
            
            
            # start find count of added place per month in range of strart_date and end-date
            added_monthly_place = dict()
            start = start_date
            while start <= end_date:
                print(start)
                try:
                    queryset = Place.objects.filter(
                        date_created__month=start.month)
                    queryset = queryset.filter(
                        date_created__year=start.year)
                    if(len(queryset) > 0):
                        added_monthly_place[f'{start.strftime("%B")}'] = len(queryset)
                except Exception as error:
                    print(error)

                start += delta

            statistics['added_monthly_place'] = added_monthly_place

            # finish find count of added place per month in range of strart_date and end-date
            
            
            # start find count of added tour per month in range of strart_date and end-date
            added_monthly_tour = dict()
            start = start_date
            while start <= end_date:
                print(start)
                try:
                    queryset = Tour.objects.filter(
                        date_created__month=start.month)
                    queryset = queryset.filter(
                        date_created__year=start.year)
                    if(len(queryset) > 0):
                        added_monthly_tour[f'{start.strftime("%B")}'] = len(queryset)
                except Exception as error:
                    print(error)

                start += delta

            statistics['added_monthly_tour'] = added_monthly_tour

            # finish find count of added tour per month in range of strart_date and end-date
            

        except Exception as error:
            return Response(f'bad request', status=status.HTTP_400_BAD_REQUEST)

        return Response(statistics, status=status.HTTP_200_OK)

    @action(detail=False, url_path='individual-statistics', methods=['POST'], permission_classes=[IsAdmin])
    def individualStatistics(self, request):
        
        try:
            statistics = defaultdict(int)

            user = User.objects.get(username=request.data['username'])
            statistics['experiences-no'] = len(user.experiences.all())
            statistics['created-tours'] = 0
            statistics['date-joined'] = user.date_joined
            print(user.tours.all())
            statistics['registered-tours'] = len(user.tours.all())
            if(user.is_special):
                special_user = SpecialUser.objects.get(user = user)
                statistics['total_revenue'] = special_user.total_revenue
                statistics['created-tours'] = len(special_user.tours.all())
            statistics['top_10_liked_experiences'] = ExperienceSerializer(
                user.experiences.all().order_by('-like_number')[:10], many=True).data
            return Response(statistics, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(f'bad request', status=status.HTTP_400_BAD_REQUEST)
