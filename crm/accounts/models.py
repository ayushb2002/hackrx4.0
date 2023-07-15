from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    manager = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='managed_team')
    # Add other fields for team as needed

    def __str__(self):
        return self.name


class Manager(models.Model):
    name = models.CharField(max_length=100)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True, related_name='manager')
    # Add other fields for manager as needed

    def __str__(self):
        return self.name


class Request(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Request by {self.employee.name}"

