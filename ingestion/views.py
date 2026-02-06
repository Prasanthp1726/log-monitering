from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

from datetime import datetime
import json

from .models import LogEntry, Alert
from .serializers import LogEntrySerializer, AlertSerializer
from django.shortcuts import render
from ingestion.models import LogEntry

def error_logs_view(request):
    logs = LogEntry.objects.select_related("user").filter(log_level="ERROR")
    return render(request, "error_logs.html", {"logs": logs})

# ======================
# FRONTEND PAGES
# ======================
def home_page(request):
    return render(request, "home.html")

def frontend(request):
    return render(request, "frontend.html")

from django.shortcuts import render
from ingestion.models import LogEntry, Alert

def dashboard(request):
    total_logs = LogEntry.objects.count()
    error_logs = LogEntry.objects.filter(log_level="ERROR").count()
    active_alerts = Alert.objects.filter(is_active=True).count()

    # 🔧 New threshold logic
    if error_logs < 3:
        system_status = "✅ OK"
    elif error_logs < 6:
        system_status = "⚠️ Warning"
    else:
        system_status = "🔴 Critical"

    context = {
        "total_logs": total_logs,
        "error_logs": error_logs,
        "active_alerts": active_alerts,
        "system_status": system_status
    }
    return render(request, "dashboard.html", context)

from django.shortcuts import render, redirect
from ingestion.models import LogEntry
from django.utils import timezone   # ✅ correct import

def send_log_page(request):
    if request.method == "POST":
        timestamp = request.POST.get("timestamp") or timezone.now()
        service = request.POST.get("service")
        log_level = request.POST.get("log_level")
        message = request.POST.get("message")

        LogEntry.objects.create(
            timestamp=timestamp,
            service=service,
            log_level=log_level,
            message=message
        )
        return redirect("send-log")

    # ✅ timezone.now() works correctly now
    return render(request, "send_log.html", {"now": timezone.now()})

def filter_logs_page(request):
    return render(request, "filter_logs.html")

def alerts_page(request):
    return render(request, "alerts.html")

def submitted_logs_page(request):
    return render(request, "filter_logs.html")

# ======================
# ANOMALY DETECTION API
# ======================
def anomaly_detection_view(request):
    try:
        queryset = LogEntry.objects.all().order_by("-timestamp")

        service = request.GET.get("service")
        log_level = request.GET.get("log_level")
        message = request.GET.get("message")

        if service:
            queryset = queryset.filter(service__iexact=service)
        if log_level:
            queryset = queryset.filter(log_level__iexact=log_level)
        if message:
            queryset = queryset.filter(message__icontains=message)

        from .ml_utils import detect_anomalies
        anomalies = detect_anomalies(queryset)
        return JsonResponse({"anomalies": anomalies})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ======================
# EMAIL ALERT FUNCTION
# ======================
def send_alert_email(alert, log):
    try:
        recipients = [e.strip() for e in alert.email_recipients.split(",") if e.strip()] \
            if alert.email_recipients else settings.ALERT_RECIPIENTS

        if not recipients:
            raise Exception("No email recipients configured")

        subject = "[ALERT] High ERROR rate 🚨"

        text_content = f"""
ANOMALY DETECTED

Service  : {log.service}
LogLevel : {log.log_level}
Message  : {log.message}
Time     : {log.timestamp}
"""

        html_content = f"""
        <html>
          <body style="font-family: Arial; background:#0f172a; color:#e5e7eb; padding:20px;">
            <h2>⚠️ ANOMALY DETECTED ⚠️</h2>
            <p><b>Service:</b> {log.service}</p>
            <p><b>Log Level:</b> {log.log_level}</p>
            <p><b>Message:</b> {log.message}</p>
            <p><b>Time:</b> {log.timestamp}</p>
          </body>
        </html>
        """

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients,
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)

        print("✅ Alert email sent to", recipients)

    except Exception as e:
        print("❌ EMAIL ERROR:", str(e))
        raise


def test_email(request, alert_id):
    try:
        alert = Alert.objects.get(id=alert_id)
        recipients = [e.strip() for e in alert.email_recipients.split(",") if e.strip()]

        email = EmailMessage(
            subject="🚨 TEST ALERT EMAIL",
            body=f"""
Hello 👋

This is a test alert email.

Alert Name       : {alert.name}
Service          : {alert.service or "Any"}
Log Level        : {alert.log_level or "Any"}
Message Contains : {alert.message_contains or "Any"}
Status           : {"Active" if alert.is_active else "Inactive"}

✅ Email system working successfully.
""",
            from_email="Alert System <prasanthp172001@gmail.com>",
            to=recipients,
        )

        sent = email.send(fail_silently=False)
        print("MAIL SEND COUNT:", sent)

        if sent == 1:
            return JsonResponse({"status": "success", "message": "Email sent"})
        else:
            return JsonResponse({"status": "failed", "message": "SMTP accepted but not sent"}, status=500)

    except Alert.DoesNotExist:
        return JsonResponse({"error": "Alert not found"}, status=404)

    except Exception as e:
        print("❌ EMAIL ERROR:", str(e))
        return JsonResponse({"error": str(e)}, status=500)


# ======================
# PAGINATION
# ======================
class LogPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


# ======================
# LOG APIs
# ======================
class LogEntryCreateView(generics.CreateAPIView):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
    permission_classes = [AllowAny]


class LogEntryListView(generics.ListAPIView):
    serializer_class = LogEntrySerializer
    permission_classes = [AllowAny]
    pagination_class = LogPagination

    def get_queryset(self):
        queryset = LogEntry.objects.all().order_by("-timestamp")

        service = self.request.query_params.get("service")
        log_level = self.request.query_params.get("log_level")
        message = self.request.query_params.get("message")

        if service:
            queryset = queryset.filter(service__iexact=service)
        if log_level:
            queryset = queryset.filter(log_level__iexact=log_level)
        if message:
            queryset = queryset.filter(message__icontains=message)

        return queryset


# ======================
# ALERT APIs
# ======================
@method_decorator(csrf_exempt, name="dispatch")
class AlertListCreateView(generics.ListCreateAPIView):
    queryset = Alert.objects.all().order_by("id")
    serializer_class = AlertSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = None


@method_decorator(csrf_exempt, name="dispatch")
class AlertRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


# ======================
# MANUAL LOG CREATE API
# ======================
@csrf_exempt
def create_log(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        data = json.loads(request.body)

        ts = parse_datetime(data.get("timestamp"))
        if not ts:
            ts = make_aware(datetime.now())
        elif ts.tzinfo is None:
            ts = make_aware(ts)

        log = LogEntry.objects.create(
            timestamp=ts,
            service=data.get("service"),
            log_level=data.get("log_level"),
            message=data.get("message")
        )

        alerts = Alert.objects.filter(is_active=True)
        for alert in alerts:
            if alert.service and alert.service != log.service:
                continue
            if alert.log_level and alert.log_level != log.log_level:
                continue
            if alert.message_contains and alert.message_contains.lower() not in log.message.lower():
                continue

            send_alert_email(alert, log)

        return JsonResponse({"status": "Log created & alert email sent"}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
