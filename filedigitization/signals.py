from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from django.core.mail import send_mail
from django.db.models.signals import m2m_changed

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
    



@receiver(post_save, sender = Document)
def on_document_created(sender, instance, created, **kwargs):
    if created:
        Backup.objects.create(
            backup_name = instance.file_name,
            backup_file = instance.file,
            requested_by = instance.uploaded_by
            
        )
        
        
        
@receiver(post_save, sender=Document)
def create_approval_and_notify(sender, instance, created, **kwargs):
    if created:
        approvers = User.objects.filter(role='manager | admin')
        if approvers:
        # for approver in approvers:
            Approval.objects.create(
                document=instance,
                approver=approvers,
                action='pending',
                comments='Awaiting approval.'
            )
            Notification.objects.create(
                recipient=approvers,
                message=f"A new document '{instance.file_name}' is awaiting your approval."
            )

        
# @receiver(post_save, sender=Document)
# def document_uploaded(sender, instance, created, **kwargs):
#     if created:
#         # Document uploaded, status is 'pending' by default
#         send_email_to_admins(instance)
#         send_email_to_uploader(instance)

# # Send email when a document's status is updated (approved, rejected, etc.)
# @receiver(post_save, sender=Document)
# def document_status_updated(sender, instance, **kwargs):
#     if not instance.pk:  # Skip if the document is not saved yet
#         return

#     # Check if status has changed and send an email to the uploader
#     if 'status' in kwargs and kwargs['status'] != instance.status:
#         send_email_to_uploader_on_status_update(instance)

#     # If the document status is approved, rejected, or change requested, send an email to the admin
#     send_email_to_admin_on_status_change(instance)
#     # send_email_to_uploader_on_status_update(instance)


# def send_email_to_admins(document):
#     admin_users = User.objects.filter(role='admin')
#     recipient_list = [user.email for user in admin_users if user.email]
#     send_mail(
#         subject="Document Submitted for Approval",
#         message=f"Document {document.file_name} has been submitted for approval.",
#         from_email="hello@fds.com",
#         recipient_list=recipient_list,
#         fail_silently=False,
#     )

# def send_email_to_uploader(document):
#     send_mail(
#         subject="Document Submitted for Approval",
#         message=f"Document {document.file_name} has been submitted for approval. Please wait for the admin's response.",
#         from_email="hello@fds.com",
#         recipient_list=[document.uploaded_by.email],  # Notify uploader
#         fail_silently=False,
#     )

# def send_email_to_uploader_on_status_update(document):
#     # Send email to the uploader based on the document status
#     if document.status == 'approved':
#         subject = "Document Approved"
#         message = f"Your document {document.file_name} has been approved."
#     elif document.status == 'rejected':
#         subject = "Document Rejected"
#         message = f"Your document {document.file_name} has been rejected."
#     elif document.status == 'change_requested':
#         subject = "Change Requested"
#         message = f"Your document {document.file_name} has been returned for changes."

#     send_mail(
#         subject=subject,
#         message=message,
#         from_email="hello@fds.com",
#         recipient_list=[document.uploaded_by.email],  # Notify uploader
#         fail_silently=False,
#     )

# def send_email_to_admin_on_status_change(document):
#     admin_users = User.objects.filter(role='admin')
#     recipient_list = [user.email for user in admin_users if user.email]
#     if not document.uploaded_by.email in recipient_list:
#         recipient_list.append(document.uploaded_by.email)
   
#     send_mail(
#         subject="Document Status Updated",
#         message=f"Document {document.file_name} has been updated to {document.status}.",
#         from_email="hello@fds.com",
#         recipient_list=recipient_list,
#         fail_silently=False,
#     )
         

# @receiver(post_save, sender=Document)
# def document_status_updated(sender, instance, created, **kwargs):
#     # Trigger only when the status is updated
#     if not created and instance.status == 'approved':
#         # Notify all accessible users about the approved document
#         recipient_list = {user.email for user in instance.accessible_users.all() if user.email}

#         # Include uploader in the email list
#         if instance.uploaded_by.email:
#             recipient_list.add(instance.uploaded_by.email)

#         # Send an email to all recipients
#         for recipient_email in recipient_list:
#             send_mail(
#                 subject="New Document uploaded",
#                 message=f"""
#                     The document '{instance.file_name}' has been approved.
#                     You now have access to view it.
#                 """,
#                 from_email="hello@fds.com",
#                 recipient_list=[recipient_email],
#                 fail_silently=False,
#             )       