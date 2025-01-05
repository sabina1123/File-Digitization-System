from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
   fieldsets = (
      (None, {"fields": ("username", "password")}),
      (("Personal info"), {"fields": ("first_name", "last_name", "email", "role")}),
      (
         ("Permissions"),
         {
            "fields": (
               "is_active",
               "is_staff",
               "is_superuser",
               "groups",
               "user_permissions",
            ),
         },
      ),
      (("Important dates"), {"fields": ("last_login", "date_joined")}),
   )
   list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
   search_fields = ('username', 'email', 'first_name', 'last_name')
   ordering = ('username',)
   
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display=['id', 'file', 'file_name', 'file_type', 'file_size', 'status', 'uploaded_by', 'uploaded_date' ]
    def accessible_users_list(self, obj):
        
        return ", ".join([user.username for user in obj.accessible_users.all()])
    
   
    accessible_users_list.short_description = 'Accessible Users'
    
  
    list_display.append('accessible_users_list')
    
    


@admin.register(MetaData)
class MetaDataAdmin(admin.ModelAdmin):
    list_display=['id', 'document', 'keywords', 'tags', 'description', 'category', 'author', 'creation_date', 'last_modified_date']
    
    

@admin.register(AuditLogs)

class AuditLogsAdmin(admin.ModelAdmin):
    list_display=['id', 'user', 'document', 'action', 'action_date', 'details']
    
    
@admin.register(ReportRequest)
class ReportRequestAdmin(admin.ModelAdmin):
   list_display = ['id', 'report_type', 'start_date', 'end_date', 'created_at', 'is_recurring', 'recurring_interval', 'user']
   
   

@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):
   list_display=['id', 'backup_name', 'backup_file', 'status', 'created_at', 'updated_at', 'restored_at', 'requested_by']