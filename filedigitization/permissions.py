from rest_framework. permissions import BasePermission, SAFE_METHODS
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# class IsAuthenticatedOrReadOnly(BasePermission):
     
#      def has_permission(self, request, view):
#          return request.user and request.user.is_authenticated

class IsAdminOnly(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"
    

class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
      if request.method in  SAFE_METHODS:
         return True
      return request.user.is_authenticated and request.user.role == 'manager'
    
    
    
    
class IsManagerOnly(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "manager"
    
    
class IsStandardUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == "standaerd_user"
    
    
class IsStandardUserOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "standard_user"
    
    
class ViewerOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
           return False
        
        role = getattr(request.user, 'role', None)
        if role != "viewer":
            return False
        
        if request.method in SAFE_METHODS:
            return True
        
        if request.method == "POST" and getattr(view, "allow_comments", False):
            return True
        
        return False
