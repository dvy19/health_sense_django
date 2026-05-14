
from rest_framework import serializers
from .models import CustomUser, UserProfile

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):

    # write_only = password will never be sent back in response
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model  = CustomUser
        fields = ["email", "password", "role"]

    def create(self, validated_data):
        # Use our custom manager to create the user
        user = CustomUser.objects.create_user(
            email    = validated_data["email"],
            password = validated_data["password"],
            role     = validated_data["role"],
        )
        return user
    

class LoginSerializer(serializers.Serializer):

    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": user.role
        }
    
class UserSerializer(serializers.ModelSerializer):

    user=serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ["user", "full_name", "gender", "city", "state", "age", "created_at", "updated_at" ]
        read_only_fields = ["created_at", "updated_at" , "user"]

    if(age := serializers.IntegerField(required=False)) is not None:
        def validate_age(self, value):
            if value < 0:
                raise serializers.ValidationError("Age cannot be negative")
            return value