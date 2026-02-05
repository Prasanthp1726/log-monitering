from django.contrib import admin
from django.urls import path, include
from ingestion.views import home_page, dashboard   # ✅ import dashboard
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# ✅ Swagger/OpenAPI schema config
schema_view = get_schema_view(
    openapi.Info(
        title="Log Monitoring API",
        default_version='v1',
        description="API documentation for Log Monitoring System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@logmonitoring.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # ✅ Home + Dashboard
    path("", home_page, name="home"),
    path("dashboard/", dashboard, name="dashboard"),

    # ✅ Admin
    path("admin/", admin.site.urls),

    # ✅ API routes
    path("api/", include("ingestion.urls")),

    # ✅ Swagger/OpenAPI endpoints
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
