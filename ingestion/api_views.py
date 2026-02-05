from rest_framework.response import Response
from rest_framework.views import APIView
from ingestion.models import LogEntry

class ErrorLogsAPI(APIView):
    def get(self, request):
        logs = LogEntry.objects.select_related("user").filter(log_level="ERROR")
        data = [{"id": log.id, "message": log.message} for log in logs]
        return Response(data)
