from rest_framework import serializers
from .models import BugReport

class BugReportSerializer(serializers.ModelSerializer):
    duplicate_of_detail = serializers.SerializerMethodField()

    class Meta:
        model = BugReport
        fields = "__all__"

    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title is too short")
        return value

    def get_duplicate_of_detail(self, obj):
        if obj.duplicate_of:
            return {
                'id':         obj.duplicate_of.id,
                'title':      obj.duplicate_of.title,
                'status':     obj.duplicate_of.status,
                'created_at': obj.duplicate_of.created_at,
            }
        return None