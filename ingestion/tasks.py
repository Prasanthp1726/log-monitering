from celery import shared_task
from ingestion.models import LogEntry, Alert
from .ml_utils import detect_anomalies
from .views import send_alert_email

@shared_task
def auto_anomaly_check():
    """
    Celery task: Runs anomaly detection on recent logs and sends alerts if suspicious entries are found.
    """
    # ✅ Step 1: Get last 500 logs (recent activity)
    logs = LogEntry.objects.select_related("user").order_by("-timestamp")[:500]

    # ✅ Step 2: Run anomaly detection
    anomalies = detect_anomalies(logs)

    # ✅ Step 3: If anomalies found, check active alerts
    if anomalies:
        for log in anomalies:
            alerts = Alert.objects.filter(is_active=True)
            for alert in alerts:
                # Service filter
                if alert.service and alert.service != log.service:
                    continue
                # Log level filter
                if alert.log_level and alert.log_level != log.log_level:
                    continue
                # Message contains filter
                if alert.message_contains and alert.message_contains.lower() not in log.message.lower():
                    continue

                # ✅ Send alert email
                send_alert_email(alert, log)


def error_log_check():
    """
    Utility function: Get only ERROR logs for manual anomaly detection or debugging.
    """
    error_logs = LogEntry.objects.select_related("user").filter(log_level="ERROR")
    # Optional: run anomaly detection on error logs
    anomalies = detect_anomalies(error_logs)
    return anomalies
