# App/management/commands/create_tasks.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from App.models import Task


class Command(BaseCommand):

    help = "Create 5000 test tasks"

    def handle(self, *args, **kwargs):

        User = get_user_model()

        user = User.objects.first()

        if not user:

            self.stdout.write(
                self.style.ERROR(
                    "No users found"
                )
            )

            return

        tasks = []

        for i in range(5000):

            tasks.append(
                Task(
                    user=user,
                    title=f"Task {i}",
                    status=(
                        "completed"
                        if i % 2 == 0
                        else "pending"
                    )
                )
            )

        Task.objects.bulk_create(tasks)

        self.stdout.write(
            self.style.SUCCESS(
                "5000 tasks created successfully"
            )
        )