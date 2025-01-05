from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['email', 'username', 'role', 'password']
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)
		return user


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        
    
    def create(self, validated_data):
        file_name = validated_data.get('file_name')
        if Document.objects.filter(file_name=file_name).exists():
            raise ValidationError({"file_name": "A document with this file name already exists."})
        
        validated_data['status'] = validated_data.get('status', 'pending')
        accessible_users = validated_data.pop('accessible_users', None)
        document =  Document.objects.create(**validated_data)
        if accessible_users:
            document.accessible_users.set(accessible_users)
        
        return document
    
    
    def update(self, instance, validated_data):
        file_name = validated_data.get('file_name', instance.file_name)
        if Document.objects.filter(file_name=file_name).exclude(id=instance.id).exists():
            raise ValidationError({"file_name": "A document with this file name already exists."})
        instance.file =validated_data.get('file',instance.file)
        instance.file_name=validated_data.get('file_name',instance.file_name)
        instance.file_type=validated_data.get('file_type',instance.file_type)
        instance.file_size = validated_data.get('file_size',instance.file_size)
        instance.status = validated_data.get('status',instance.status)
        instance.uploaded_by = validated_data.get('uploaded_by',instance.uploaded_by)
        instance.uploaded_date= validated_data.get('uploaded_date',instance.uploaded_date)
        accessible_users = validated_data.get('accessible_users', None)
        if accessible_users is not None:
            # Replace existing relationships
            instance.accessible_users.set(accessible_users)
        instance.save()
        
        
        return instance
                
        
    # def save(self, **kwargs):
    #     validated_data = self.validated_data
    #     total_number = self.Meta.model.objects.filter(file_name = validated_data.get('file_name')).count()
        
    #     if total_number>0:
    #         raise serializers.ValidationError('Document Already Exists')
        
    #     document = self.Meta.model(**validated_data)
    #     document.save()
    #     return document

class MetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaData
        fields = '__all__'
        
        
class AuditLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLogs
        fields = '__all__'
        

class ReportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportRequest
        fields = '__all__'
        
    
class BackupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Backup
        fields = '__all__'
