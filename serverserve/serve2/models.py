from django.db import models

class Employee(models.Model):
    employee_id = models.CharField(max_length=10, unique=True)
    employee_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.employee_name


class WorkSession(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.name} from {self.start_time} to {self.end_time if self.end_time else 'Ongoing'}"

    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None
