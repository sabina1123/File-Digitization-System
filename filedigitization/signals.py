from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from django.core.mail import send_mail

@receiver(post_save, sender=Document)

def on_document_created(sender, instance, created, **kwargs):
    
    if created:
        AuditLogs.objects.create(
            user = instance.uploaded_by,
            document = instance,
            action = 'upload',
            details=f'Document "{instance.file_name}" uploaded.',
        )
        
        
    
    
@receiver(post_delete, sender = Document)
def on_document_deleted(sender, instance, **kwargs):
    AuditLogs.objects.create(
        user = instance.uploaded_by,
        document = None,
        action = 'delete',
        details=f'Document "{instance.file_name}" was deleted.',
    )
    
# @receiver(post_save, sender=Document)
# def on_document_updated(sender, instance, created, **kwargs):
    
#     if not created:  # This indicates it's an update, not a creation
#         AuditLogs.objects.create(
#             user=instance.uploaded_by,
#             document=instance,
#             action='update',
#             details=f'Document "{instance.file_name}" was updated.',
#         )
        
    
    


@receiver(post_save, sender=Document)
def on_document_created(sender, instance,  **kwargs):
    print('Document signal was trigger')
    send_mail(
       subject= "New Document Uploaded" ,
       message = """
         A new document "{instance.file_name}" has been uploaded by {instance.uploaded_by.username}.
    You have access to view it.
        """,
       from_email = "hello@fds.com",
       recipient_list=[instance.uploaded_by.email for user in instance.accessible_users.all()] 
       
        )