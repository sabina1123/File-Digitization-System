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
        field = '__all__'
        


class MetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaData
        field = '__all__'
        
        
class AuditLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLogs
        field = '__all__'
