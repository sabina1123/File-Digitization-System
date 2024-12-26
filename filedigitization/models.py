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
    # email = models.EmailField(unique=True)
    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS=['username']
    
    def __str__(self):
        return f"{self.username}-{self.role}"
    
    
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
    
    
    def __str__(self):
        return f"file name is {self.file_name}"    
        
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
    
    

class ReportRequest(models.Model):
    REPORT_CHOICES =(
        ('usage', 'Usage Report'),
        ('access', 'Access Patterns Report')
    )
    report_type = models.CharField(max_length=50, choices=REPORT_CHOICES)
    start_date = models.DateField()
    end_date= models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_recurring = models.BooleanField(default = False)
    recurring_interval = models.CharField(
        max_length=50,
        choices=(
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly')
        ), null = True, blank = True) 
    user =   models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.report.type} Report ({self.start_date} - {self.end_date})"
    
    
    
class Backup(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        )
    backup_name = models.CharField(max_length=255)
    backup_file = models.FileField(upload_to = 'backups/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    next_scheduled_backup = models.DateTimeField(null=True, blank=True)
    restored_at = models.DateTimeField(null=True, blank=True)
    requested_by = models.ForeignKey(
      User,
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='backup_requests',
    )

    def __str__(self):
        return f"Backup: {self.backup_name} ({self.status})"
    

    

