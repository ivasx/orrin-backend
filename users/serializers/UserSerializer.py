from rest_framework import serializers
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'date_of_birth', 'gender')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        temp_username = f"user_{uuid.uuid4().hex[:10]}"

        user = User.objects.create_user(
            username=temp_username,
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            date_of_birth=validated_data.get('date_of_birth'),
            gender=validated_data.get('gender')
        )
        return user