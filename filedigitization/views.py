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
   permission_classes = [IsAuthenticatedOrReadOnly]
   


class MetaDataViewSet(viewsets.ModelViewSet):
   queryset = MetaData.objects.all()
   serializer_class = MetaDataSerializer
   filter_backends = [filters.SearchFilter]
   search_fields = ['keywords']
   
class AuditLogsViewSet(viewsets.ModelViewSet):
   queryset = AuditLogs.objects.all()
   serializer_class = AuditLogsSerializer
   
   
   
class ReportRequestViewSet(viewsets.ModelViewSet):
   queryset = ReportRequest.objects.all()
   serializer_class= ReportRequestSerializer
   
   
   
class BackupViewSet(viewsets.ModelViewSet):
   queryset = Backup.objects.all()
   serializer_class = BackupSerializer

