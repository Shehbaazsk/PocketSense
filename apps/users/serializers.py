from rest_framework import serializers

from apps.users.models import  User


class UserRegisterSerializers(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(
        write_only=True, required=True, label="Password Confirmation"
    )
    

    class Meta:
        model = User
        fields = ["email", "password", "password2",
                   "first_name","college","semester","default_payment_methods"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                "The password field does not match")
        del attrs["password2"]


        return attrs
    def create(self, validated_data):
        user = User.objects.create_user( **validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name","college","semester","default_payment_methods"]



class UserAllDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('password', 'last_login', 'is_superuser',
                   'is_staff',   'groups', 'user_permissions', 'is_delete')


