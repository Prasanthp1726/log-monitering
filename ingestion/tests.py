from django.test import TestCase, Client
from django.urls import reverse
from ingestion.models import LogEntry, Alert
from ingestion.tasks import auto_anomaly_check

class LogEntryTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a sample log
        self.log = LogEntry.objects.create(
            service="auth",
            log_level="ERROR",
            message="Payment failed"
        )
        # Create a sample alert
        self.alert = Alert.objects.create(
            service="auth",
            log_level="ERROR",
            message_contains="Payment",
            is_active=True
        )

    def test_log_creation(self):
        # ✅ Check model fields
        self.assertEqual(self.log.service, "auth")
        self.assertEqual(self.log.log_level, "ERROR")

    def test_dashboard_view(self):
        # ✅ Check dashboard loads correctly
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")

    def test_auto_anomaly_check_task(self):
        # ✅ Run anomaly detection task manually
        auto_anomaly_check()

        # After running, check if alerts exist
        alerts = Alert.objects.filter(is_active=True)
        self.assertTrue(alerts.exists())
