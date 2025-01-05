from rest_framework import serializers
from django.db import transaction

from apps.accounts.users.serializers import UserRegisterSerializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializers()  
    
    class Meta:
        model = Student
        fields = ['user', 'college', 'semester', 'default_payment_method']


    def create(self, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop('user')
            user = UserRegisterSerializers().create(user_data)
            student = Student.objects.create(user=user, **validated_data)
        return student