from rest_framework import serializers
from django.db import transaction

from apps.accounts.users.serializers import UserAllDetailsSerializer, UserRegisterSerializers
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
    
class ListGetStudentSerializers(serializers.ModelSerializer):
    user = UserAllDetailsSerializer()
    
    class Meta:
        model = Student
        fields = '__all__'
    
class UpdateStudentSerializers(serializers.ModelSerializer):
    user = UserAllDetailsSerializer()

    class Meta:
        model = Student
        fields = "__all__"
        

    def update(self, instance, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop('user')
            if user_data:
                user_serializer = UserAllDetailsSerializer(instance.user, data=user_data,partial=True)
                user_serializer.is_valid(raise_exception=True)
                user_serializer.save()
            
            for attr, value in validated_data.items():
                if hasattr(instance, attr) and getattr(instance, attr) != value:
                    setattr(instance, attr, value)
            instance.save()
        return instance
    