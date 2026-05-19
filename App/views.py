import time

from django.core.cache import cache

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer


class DashboardView(ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    CACHE_TIMEOUT = 60 * 10

    def _build_dashboard_data(self, user):

        total_tasks = Task.objects.filter(
            user=user
        ).count()

        completed_tasks = Task.objects.filter(
            user=user,
            status="completed"
        ).count()

        pending_tasks = Task.objects.filter(
            user=user,
            status="pending"
        ).count()

        completion_percentage = 0

        if total_tasks > 0:

            completion_percentage = round(
                (completed_tasks / total_tasks) * 100,
                1
            )

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "completion_percentage": completion_percentage,
        }

    def list(self, request):

        start_time = time.time()

        cache_key = (
            f"dashboard:v1:{request.user.uuid}"
        )

        dashboard_data = cache.get(cache_key)

        if not dashboard_data:

            dashboard_data = self._build_dashboard_data(
                request.user
            )

            cache.set(
                cache_key,
                dashboard_data,
                timeout=self.CACHE_TIMEOUT
            )

        end_time = time.time()

        print(
            f"Dashboard generated in: "
            f"{end_time - start_time:.4f} seconds"
        )

        return Response(dashboard_data)