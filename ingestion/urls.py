from django.urls import path
from .views import (
    # FRONTEND VIEWS
    home_page,
    frontend,
    send_log_page,
    filter_logs_page,
    alerts_page,
    submitted_logs_page,
    dashboard,   # ✅ include here

    # ALERT VIEWS & APIs
    test_email,
    AlertListCreateView,
    AlertRetrieveUpdateDestroyView,

    # LOG VIEWS & APIs
    create_log,
    LogEntryListView,
    anomaly_detection_view
)

# ======================
# FRONTEND PAGES (HTML)
# ======================
frontend_urls = [
    path("", home_page, name="home"),
    path("viewer/", frontend, name="viewer"),
    path("form/", send_log_page, name="send-log"),
    path("filter/", filter_logs_page, name="filter"),
    path("alerts/", alerts_page, name="alerts"),
    path("submitted/", submitted_logs_page, name="submitted"),
    path("dashboard/", dashboard, name="dashboard"),
    
]

# ======================
# LOG APIs (JSON)
# ======================
log_api_urls = [
    path("logs/", create_log, name="create-log"),  # manual POST API
    path("logs/view/", LogEntryListView.as_view(), name="logs"),  # paginated GET API
    path("logs/anomalies/", anomaly_detection_view),  # ML anomaly detection
]

# ======================
# ALERT APIs (JSON)
# ======================
alert_api_urls = [
    path("alerts/api/", AlertListCreateView.as_view(), name="alert-list-create"),
    path("alerts/api/<int:pk>/", AlertRetrieveUpdateDestroyView.as_view(), name="alert-detail"),
    path("test-alert-email/<int:alert_id>/", test_email, name="test-alert-email"),
]

# ======================
# FINAL URLPATTERNS
# ======================
urlpatterns = frontend_urls + log_api_urls + alert_api_urls
