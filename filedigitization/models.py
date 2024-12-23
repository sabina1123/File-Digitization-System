from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES=(
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('standard_user', 'Standard User'),
        ('viewer', 'Viewer'),
        )
    
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, null=True, blank = True)
    
    def __str__(self):
        return f"{self.user.username}-{self.role}"
    
    
class Document(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('change_requested', 'Change Requested'),
    )
    file = models.FileField(upload_to='documents/')
    file_name=models.CharField(max_length=100)
    file_type=models.CharField(max_length=50)
    file_size = models.PositiveIntegerField()
    status = models.CharField(max_length = 100, choices=STATUS_CHOICES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_date= models.DateTimeField(auto_now_add=True)
    
        
class MetaData(models.Model):
    CATEGORY_CHOICE=(
        ('personal', 'Personal'),
        ('corporate', 'Corporate'),
        ('educational', 'Educational'),
        ('government', 'Government'),
        ('project', 'Project'),
        ('legal', 'Legal'),
        )
    
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    keywords = models.TextField(blank = True)   
    tags = models.TextField(blank = True)    
    description = models.TextField(blank = True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICE, blank = True)
    author = models.CharField(max_length=255, blank=True)
    creation_date = models.DateTimeField(null=True, blank=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"MetaData for {self.Document.file_name}"
    
    

class AuditLogs(models.Model):
    ACTION_DETAILS=(
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('upload', 'Upload')
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    action = models.CharField(max_length=100, choices=ACTION_DETAILS)
    action_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)
    
    
    

    

