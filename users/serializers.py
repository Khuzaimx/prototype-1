from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, CRAssignment


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password_confirm')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }
    
    def validate_email(self, value):
        """Validate email domain."""
        if not value.endswith('@giki.edu.pk'):
            raise serializers.ValidationError('Email must be from giki.edu.pk domain')
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        # Role will be auto-assigned based on CR assignments
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate_email(self, value):
        """Validate email domain."""
        if not value.endswith('@giki.edu.pk'):
            raise serializers.ValidationError('Email must be from giki.edu.pk domain')
        return value
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password.')
        
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'role', 'created_at', 'updated_at')
        read_only_fields = ('id', 'role', 'created_at', 'updated_at')


class CRAssignmentSerializer(serializers.ModelSerializer):
    """Serializer for CR assignments."""
    assigned_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = CRAssignment
        fields = ('id', 'email', 'assigned_by', 'assigned_at', 'is_active')
        read_only_fields = ('id', 'assigned_by', 'assigned_at')
    
    def validate_email(self, value):
        """Validate email domain."""
        if not value.endswith('@giki.edu.pk'):
            raise serializers.ValidationError('Email must be from giki.edu.pk domain')
        return value
