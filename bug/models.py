from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class BugReport(models.Model):
    SEVERITY_CHOICES = (
        ('critical', 'Critical'),
        ('medium', 'Medium'),
        ('High', 'High'),
        ('low', 'Low'),
    )

    Status_choices = (
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField( max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=Status_choices, default="open")
    reporter_email = models.EmailField()
    reporter_name = models.CharField(max_length=20)
    reporter_info = models.TextField(blank=True, null=True)
    reporter_phone_number = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
