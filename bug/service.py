from .models import BugReport

class BugService:

    @staticmethod
    def create_bug(validated_data):
        return BugReport.objects.create(**validated_data)

    @staticmethod
    def list_bugs(filters=None):
        queryset = BugReport.objects.all()

        if filters:
            if filters.get("severity"):
                queryset = queryset.filter(severity=filters.get("severity"))
            if filters.get("status"):
                queryset = queryset.filter(status=filters.get("status"))

        return queryset.order_by("-created_at")