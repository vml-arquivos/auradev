"""
Serializers for Core app.
"""
from rest_framework import serializers
from .models import User, Notification


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'bio', 'avatar', 'phone', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserDetailSerializer(UserSerializer):
    """
    Detailed serializer for User model.
    """
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['date_joined', 'last_login']
        read_only_fields = UserSerializer.Meta.read_only_fields + ['date_joined', 'last_login']


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    """
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'title', 'message', 'priority',
            'status', 'link', 'created_at', 'read_at'
        ]
        read_only_fields = ['id', 'created_at', 'read_at']
