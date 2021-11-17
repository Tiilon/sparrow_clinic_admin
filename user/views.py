from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate, login
from .models import *
from .serializers import *
import datetime
from dateutil import parser
from rest_framework.views import APIView
# import os
# import json
# import requests

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['role'] = user.role
        # token['profile'] = user.profile
        details = {
            'token': token,
            'profile': user.profile
        }
        # ...

        return token

# @api_view(['POST'])
# def sign_in(request):
#     email= request.data.get('email')
#     password = request.data.get('password')

#     if not email:
#         return Response({'error': 'Email Field Required'})
#     if not password:
#         return Response({'error': 'Password Field Required'})

#     try:
#         user = authenticate(request, email=email, password=password)

#         if user is not None and user.is_active:
#             login(request, user)
#             user.token = ''
#             user.save()

#             url = f'http://{request.get_host()}/jwt/token/'
#             payload = {
#                 'first_name':user.first_name,
#                 'last_name':user.last_name,
#                 'email':user.email,
#                 'role':user.role,
#                 }
#             headers = {
#                 'content-type':'application/x-www-form-urlencoded',
#                 'Authorization': f'Bearer {os.environ.get("BASE_64_MASHUP")}'
#             }
#             myrequest = requests.post(url, payload, headers=headers)

#             return Response({
#                 'token': json.loads(myrequest.text),
#                 'user': {
#                     'first_name':user.first_name,
#                     'last_name':user.last_name,
#                     'profile':user.profile,
#                     'email':user.email,
#                     'role':user.role,
#                 }
#             })
#         else:
#             return Response({'error': 'Credentials do not match or user is inactive'})
#     except User.DoesNotExist:
#         return Response({'error': 'User does not exist'})

class MyTokenObtainPairView(TokenObtainPairView):
    # permission_classes = [AllowAny]
    # authentication_classes = [JWTAuthentication]
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def blacklist_token_view(request):
    try:
        refresh_token = request.data['refresh_token']
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', "POST"])
def schedule(request):
    if request.method == 'GET':
        schedules = Schedule.objects.filter(created_by=request.user)
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        description = request.data.get('description')
        date = request.data.get('date')
        # end_date = request.data.get('end_date')
        input_start_time = request.data.get('start_time')
        start_time = parser.isoparse(input_start_time)
        str_start_time = datetime.datetime.strftime(start_time, "%H:%M %p")
        input_end_time = request.data.get('end_time')
        end_time = parser.isoparse(input_end_time)
        str_end_time = datetime.datetime.strftime(end_time, "%H:%M %p")
        
        new_schedule = Schedule.objects.create(
            description=description, 
            date=date,
            # end_date=end_date,
            start_time=datetime.datetime.strptime(str_start_time, '%H:%M %p'),
            end_time=datetime.datetime.strptime(str_end_time, '%H:%M %p'),
            created_by = request.user
        )

    return Response(ScheduleSerializer(new_schedule).data, status=status.HTTP_201_CREATED)