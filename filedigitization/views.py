from django.shortcuts import render
from .serializers import *
from rest_framework import status, generics , viewsets
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate, login , logout
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from .permissions import *
from django_filters import rest_framework as filter
from rest_framework.decorators import action
from django.core.mail import send_mail
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification as FCMNotification



# Create your views here.

class RegistrationAPIView(APIView):
   def post(self, request):
      serializer = UserSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response({'message': 'User registered successfully.'},status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

class LoginAPIView(APIView):
   def post(self, request):
      username = request.data.get('username')
      password = request.data.get('password')
      if not username or not password:
         raise AuthenticationFailed('Both username and password are required')
      user = authenticate(request, username=username, password=password)
      if user is not None:
         login(request, user)
         token, created = Token.objects.get_or_create(user=user)
         return Response({'token': token.key, 'username': user.username, 'role': user.role})
      raise AuthenticationFailed('Invalid username or password')

class LogoutAPIView(APIView):
   permissions_classes = [IsAuthenticated]
   def post(self, request):
      username = request.data.get('username')
      password = request.data.get('password')
      if not(username and password):
         return Response({'detail':'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
      user = authenticate(username=username, password=password)
      if user is not None:
         logout(request)
         try:
            token = Token.objects.get(user=user)
            token.delete()
            return Response({'detail': 'Successfully logged out.'})
         except Token.DoesNotExist:
            return Response({'detail': 'Token does not exist.'}, status=status.HTTP_404_NOT_FOUND)
      else:
         return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)
     



class DocumentViewSet(viewsets.ModelViewSet):
   
   queryset = Document.objects.all()
   serializer_class = DocumentSerializer
   pagination_class = PageNumberPagination
   filter_backends = [filters.SearchFilter, filter.DjangoFilterBackend]
   search_fields = ['file_name', 'uploaded_date']
   permission_classes = [IsAdminOnly|IsManagerOnly|IsStandardUserOnly|ViewerOnly]
    


class MetaDataViewSet(viewsets.ModelViewSet):
   queryset = MetaData.objects.all()
   serializer_class = MetaDataSerializer
   pagination_class = PageNumberPagination
   filter_backends = [filters.SearchFilter, filter.DjangoFilterBackend]
   search_fields = ['keywords', 'tags']
   permission_classes= [IsAdminOnly|IsManagerOnly|IsStandardUserOnly|ViewerOnly]
   
   
class AuditLogsViewSet(viewsets.ModelViewSet):
   queryset = AuditLogs.objects.all()
   serializer_class = AuditLogsSerializer
   pagination_class = PageNumberPagination
   filter_backends = [filters.SearchFilter, filter.DjangoFilterBackend]
   search_fields = ['action', 'action_date']
   permission_classes = [IsAdminOnly|IsManagerOnly]
   
   
   
class ReportRequestViewSet(viewsets.ModelViewSet):
   queryset = ReportRequest.objects.all()
   serializer_class= ReportRequestSerializer
   pagination_class = PageNumberPagination
   filter_backends = [filters.SearchFilter, filter.DjangoFilterBackend]
   search_fields = ['report_type', 'recurring_interval']
   permission_classes = [IsAdminOnly|IsManagerOnly]
   
   
   
class BackupViewSet(viewsets.ModelViewSet):
   queryset = Backup.objects.all()
   serializer_class = BackupSerializer
   pagination_class = PageNumberPagination
   filter_backends = [filters.SearchFilter, filter.DjangoFilterBackend]
   search_fields = ['backup_name', 'status']
   permission_classes = [IsAdminOnly|IsManagerOnly]
   
   

class NotificationViewSet(viewsets.ModelViewSet):
   queryset = Notification.objects.all()
   serializer_class = NotificationSerializer
   def perform_create(self, serializer):
        # Save the notification instance
      notification = serializer.save()

        # Prepare the FCM message
      message = Message(
         notification=FCMNotification(
         title=notification.title,
         body=notification.message,
            ),
            # Optionally, you can include data payload here
         data={
                'notification_type': notification.notification_type,
                'notification_id': str(notification.id),  # Include ID if needed
            },
        )

        # Send the message to all active devices associated with users
      devices = FCMDevice.objects.filter(user__notificationtoken__is_active=True)
      if devices.exists():
         devices.send_message(message)


class NotificationTokenAPIView(APIView):
   def post(self, request):
      serializer = NotificationTokenSerializer(data= request.data)
      if serializer.is_valid():
         serializer.save()
         return Response({"status_code": 201, "message": "Notification token created"}, status=status.HTTP_201_CREATED)
      return Response({"status_code": 400, "message": "There are errors in the entries made."}, status=status.HTTP_400_BAD_REQUEST)
      
# class NotificationTokenViewSet(viewsets.ModelViewSet):
#    queryset = NotificationToken.objects.all()
#    serializer_class = NotificationTokenSerializer  


class RegisterDeviceView(APIView):
    def post(self, request):
        registration_id = request.data.get('registration_id')  # Get the FCM token from the request
        user = request.user  # Assuming the user is authenticated

        if not registration_id:
            return Response({"error": "Registration ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Create or update the FCMDevice instance
        device, created = FCMDevice.objects.get_or_create(
            registration_id=registration_id,
            user=user,
            defaults={'active': True, 'type': request.data.get('device_type', 'unknown')}
        )

        if not created:
            device.active = True  # Ensure the device is active
            device.save()

        return Response({"status": "Device registered successfully"}, status=status.HTTP_201_CREATED)