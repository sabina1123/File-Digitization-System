from rest_framework. permissions import BasePermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class IsAuthenticatedOrReadOnly(BasePermission):
     
     def has_permission(self, request, view):
         return request.user and request.user.is_authenticated