
from django.db import models

# Create your models here.
class BugReport(models.Model):
    SEVERITY_CHOICES = (
        ('critical', 'Critical'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('low', 'Low'),
    )

    STATUS_CHOICES = (
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField( max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    reporter_email = models.EmailField()
    reporter_name = models.CharField(max_length=100)
    reporter_info = models.TextField(blank=True, null=True)
    reporter_phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bug_report'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
