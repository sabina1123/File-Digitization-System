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
   
   # @action(detail=True, methods=['post'], url_path='approve')
   # def approve_document(self, request, pk=None):
   #      document = self.get_object()
        
   #      if document.status != 'pending':
   #          return Response({"detail": "Document has already been approved or rejected."}, status=status.HTTP_400_BAD_REQUEST)
        
   #      # Set the document status to 'approved'
   #      document.status = 'approved'
   #      document.save()

   #      # Send email to the uploader
   #      send_mail(
   #          subject="Document Approved",
   #          message=f"Document {document.file_name} has been approved.",
   #          from_email="hello@fds.com",
   #          recipient_list=[document.uploaded_by.email],  # Notify uploader
   #          fail_silently=False,
   #      )

   #      return Response({"detail": "Document approved successfully."}, status=status.HTTP_200_OK)

   #  # Custom action to reject a document
   # @action(detail=True, methods=['post'], url_path='reject')
   # def reject_document(self, request, pk=None):
   #      document = self.get_object()

   #      if document.status != 'pending':
   #          return Response({"detail": "Document has already been approved or rejected."}, status=status.HTTP_400_BAD_REQUEST)
        
   #      # Set the document status to 'rejected'
   #      document.status = 'rejected'
   #      document.save()

   #      # Send email to the uploader
   #      send_mail(
   #          subject="Document Rejected",
   #          message=f"Document {document.file_name} has been rejected.",
   #          from_email="hello@fds.com",
   #          recipient_list=[document.uploaded_by.email],  # Notify uploader
   #          fail_silently=False,
   #      )

   #      return Response({"detail": "Document rejected successfully."}, status=status.HTTP_200_OK)

   #  # Custom action for submitting document for approval (change status to pending)
   # @action(detail=True, methods=['post'], url_path='submit-approval-request')
   # def submit_for_approval(self, request, pk=None):
   #      document = self.get_object()
        
   #      # Set the document status to 'pending' for approval
   #      document.status = 'pending'
   #      document.save()
        
   #      admin_users = User.objects.filter(role='admin')
   #      print(admin_users)
        
   #      # Collect the emails of admin users
   #      recipient_list = [user.email for user in admin_users if user.email]

   #      # Send email to admin users about the document submission
   #      send_mail(
   #          subject="Document Submitted for Approval",
   #          message=f"Document {document.file_name} has been submitted for approval.",
   #          from_email="hello@fds.com",
   #          recipient_list=recipient_list,
   #          fail_silently=False,
   #      )

   #      return Response({"detail": "Document submitted for approval."}, status=status.HTTP_200_OK)

    


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

