from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


router = routers.SimpleRouter()
router.register(r'documents', DocumentViewSet, basename='documents')
router.register(r'metadatas',MetaDataViewSet, basename='metadata')
router.register(r'auditlogs', AuditLogsViewSet, basename='auditlogs')
router.register(r'reportrequest', ReportRequestViewSet, basename = "reportrequest")
router.register(r'backup', BackupViewSet, basename= 'backup')


urlpatterns = router.urls+[
   path('register/', RegistrationAPIView.as_view(), name='user-registration'),
   path('login/', LoginAPIView.as_view(), name='user-login'),
   path('logout/', LogoutAPIView.as_view(), name='user-logout'),
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   
   
]
if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
