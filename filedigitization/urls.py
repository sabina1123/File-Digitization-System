from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
   
router = routers.SimpleRouter()
router.register(r'documents', DocumentViewSet, basename='documents')
router.register(r'metadatas',MetaDataViewSet, basename='metadata')
router.register(r'auditlogs', AuditLogsViewSet, basename='auditlogs')
urlpatterns = router.urls+[
   path('register/', RegistrationAPIView.as_view(), name='user-registration'),
   path('login/', LoginAPIView.as_view(), name='user-login'),
   path('logout/', LogoutAPIView.as_view(), name='user-logout'),
   
   
]
if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
