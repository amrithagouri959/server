from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'employee_name', 'username', 'password')
    search_fields = ('employee_id', 'employee_name', 'username')
    readonly_fields = ('password',)  # Make password field read-only for security


