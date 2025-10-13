from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone", "full_name", "image", "fcm_token", )
        extra_kwargs = {
            "phone": {"required": False},
            "full_name": {"required": False},
            "image": {"required": False},
            "fcm_token": {"required": False},
        }
