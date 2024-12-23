from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display=['id', 'file', 'file_name', 'file_type', 'file_size', 'status', 'uploaded_by', 'uploaded_date' ]
    
    


@admin.register(MetaData)
class MetaDataAdmin(admin.ModelAdmin):
    list_display=['id', 'document', 'keywords', 'tags', 'description', 'category', 'author', 'creation_date', 'last_modified_date']
    
    

@admin.register(AuditLogs)

class AuditLogsAdmin(admin.ModelAdmin):
    list_display=['id', 'user', 'document', 'action', 'action_date', 'details']
