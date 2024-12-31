from rest_framework import serializers
from .models import *


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
        
    def save(self, **kwargs):
        validated_data = self.validated_data
        total_number = self.Meta.model.objects.filter(file_name = validated_data.get('file_name'))
        
        if total_number>0:
            raise serializers.ValidationError('Document Already Exists')
        
        document = self.Meta.model(**validated_data)
        document.save()
        return document

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
