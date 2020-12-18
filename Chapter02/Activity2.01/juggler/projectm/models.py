from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=50, help_text="Project Name")
    creation_time = models.DateTimeField(auto_now_add=True, help_text="Project creation time.")
    completion_time = models.DateTimeField(null=True, help_text="Project completion time")

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100,
                             help_text="Task title")
    description = models.TextField(help_text="Task description")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    time_estimate = models.IntegerField(help_text="Time in hours required to complete the task.")
    completed = models.BooleanField(default=False, help_text="Task completion status")

    def __str__(self):
        return self.title