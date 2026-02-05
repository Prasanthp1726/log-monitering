from django.db import models

class LogEntry(models.Model):
    # Proper datetime field for accurate filtering and sorting
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)  # ✅ auto_now_add for creation time

    # Service name (indexed for fast filtering)
    service = models.CharField(max_length=100, db_index=True)

    # Log level (INFO, WARNING, ERROR, DEBUG)
    log_level = models.CharField(max_length=20, db_index=True)

    # Log message text
    message = models.TextField()

    def __str__(self):
        return f"[{self.timestamp}] {self.service} - {self.log_level}"


class Alert(models.Model):
    name = models.CharField(max_length=100)
    service = models.CharField(max_length=100, blank=True, null=True)
    log_level = models.CharField(max_length=20, blank=True, null=True)
    message_contains = models.CharField(max_length=255, blank=True, null=True)
    email_recipients = models.TextField()  # Comma-separated emails
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
