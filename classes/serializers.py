from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ClassSchedule, ClassAttachment, AlarmSettings

User = get_user_model()


class ClassAttachmentSerializer(serializers.ModelSerializer):
    """Serializer for class attachments."""
    file_size_mb = serializers.ReadOnlyField()
    
    class Meta:
        model = ClassAttachment
        fields = ['id', 'file', 'original_filename', 'file_size', 'file_size_mb', 'uploaded_at']
        read_only_fields = ['id', 'file_size', 'uploaded_at']


class ClassScheduleSerializer(serializers.ModelSerializer):
    """Serializer for class schedules."""
    created_by = serializers.StringRelatedField(read_only=True)
    attachments = ClassAttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = ClassSchedule
        fields = [
            'id', 'created_by', 'subject', 'venue', 'date', 'time', 
            'note', 'attachments', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create class schedule with current user as creator."""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ClassScheduleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating class schedules."""
    
    class Meta:
        model = ClassSchedule
        fields = ['subject', 'venue', 'date', 'time', 'note']
    
    def create(self, validated_data):
        """Create class schedule with current user as creator."""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ClassScheduleListSerializer(serializers.ModelSerializer):
    """Serializer for listing class schedules."""
    created_by = serializers.StringRelatedField(read_only=True)
    attachment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ClassSchedule
        fields = [
            'id', 'created_by', 'subject', 'venue', 'date', 'time', 
            'note', 'attachment_count', 'created_at', 'updated_at'
        ]
    
    def get_attachment_count(self, obj):
        """Get count of attachments for this class."""
        return obj.attachments.count()


class ClassAttachmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating class attachments."""
    
    class Meta:
        model = ClassAttachment
        fields = ['file']
    
    def create(self, validated_data):
        """Create attachment with metadata."""
        file = validated_data['file']
        validated_data['original_filename'] = file.name
        validated_data['file_size'] = file.size
        validated_data['class_schedule_id'] = self.context['class_schedule_id']
        return super().create(validated_data)


class AlarmSettingsSerializer(serializers.ModelSerializer):
    """Serializer for alarm settings."""
    
    class Meta:
        model = AlarmSettings
        fields = ['id', 'is_enabled', 'alarm_minutes_before', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create alarm setting with current user."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AlarmSettingsUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating alarm settings."""
    
    class Meta:
        model = AlarmSettings
        fields = ['is_enabled', 'alarm_minutes_before']
