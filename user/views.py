from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from .serializers import *
import datetime
from dateutil import parser

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
        # ...

        return token

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