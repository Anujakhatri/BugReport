from rest_framework import serializers
from .models import BugReport

class BugReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReport
        fields = "__all__"

    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title is too short")
        return value