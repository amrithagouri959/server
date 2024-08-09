from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Employee
from django.db import IntegrityError
from django.db.models import Q
import os

def view_all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'view_all_emp.html', context)

def add_emp(request):
    if request.method == 'POST':
        employee_id = request.POST['employee_id']
        employee_name = request.POST['employee_name']
        username = request.POST['username']
        password = request.POST['password']
        verify_password = request.POST['verify_password']

        if password != verify_password:
            return HttpResponse('Passwords do not match')

        if Employee.objects.filter(employee_id=employee_id).exists():
            return HttpResponse('Employee ID already exists')

        try:
            new_emp = Employee(
                employee_id=employee_id,
                employee_name=employee_name,
                username=username,
                password=password,
            )
            new_emp.save()
            return HttpResponse('Employee added successfully')
        except IntegrityError:
            return HttpResponse('An error occurred. Employee not added.')
    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("An exception occurred! Employee has not been added")


def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = get_object_or_404(Employee, employee_id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee removed successfully")
        except:
            return HttpResponse("Please enter a valid Emp ID")
    else:
        emps = Employee.objects.all()
        context = {
            'emps': emps
        }
        return render(request, 'remove_emp.html', context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(employee_name__icontains=name) | Q(username__icontains=name))

        context = {
            'emps': emps
        }
        return render(request, 'view_all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An exception occurred')



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt  # Disables CSRF for testing;
def authenticate(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            employee = Employee.objects.get(username=username, password=password)
            if employee:
                print(f"Log: Employee {username} found!")
                return JsonResponse({'status':'success','message':'Server Authentication Successful'})

        except Employee.DoesNotExist:
            print(f"Log: Employee {username} not found")
            return JsonResponse({'status': 'error', 'message': 'User does not exist'})

        except json.JSONDecodeError:
            return JsonResponse({'status':'error','message':'Invalid JSON'})
        return JsonResponse({'status': 'error', 'message': 'Invalid Request'})
    else:
        return HttpResponse("Invalid request method", status=405)


    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #
    #     print(f"Got request for username:{username}")  # LOG
    #
    #     try:
    #         employee = Employee.objects.get(username=username, password=password)
    #         if employee:
    #             print(f"Employee {username} found!")
    #         return serve_file(r"C:\Users\DELL\success.html")
    #     except Employee.DoesNotExist:
    #         return serve_file(r"C:\Users\DELL\failure.html")
    # else:
    #     return HttpResponse("Invalid request method", status=405)


def serve_file(file_path):
    if not os.path.exists(file_path):
        return HttpResponse("File not found", status=404)

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return HttpResponse(content, content_type="text/html")
    except Exception as e:
        return HttpResponse(f"Error serving file: {e}", status=500)



from django.utils.dateparse import parse_datetime
from .models import WorkSession
@csrf_exempt  # For testing purposes, be cautious with CSRF in production
def start_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        employee_id = data.get('employee_id')
        start_time = parse_datetime(data.get('start_time'))

        if employee_id and start_time:
            try:
                employee = Employee.objects.get(id=employee_id)
                session = WorkSession.objects.create(employee=employee, start_time=start_time)
                print(f"Log: Employee {id} started session!")
                return JsonResponse({'status': 'success', 'session_id': session.id})
            except Employee.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Employee not found'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt  # For testing purposes, be cautious with CSRF in production
def end_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        employee_id = data.get('employee_id')
        start_time = parse_datetime(data.get('start_time'))
        end_time = parse_datetime(data.get('end_time'))

        if employee_id and start_time and end_time:
            try:
                employee = Employee.objects.get(id=employee_id)
                session = WorkSession.objects.get(employee=employee, start_time=start_time, end_time__isnull=True)
                session.end_time = end_time
                session.save()
                print(f"Log: Employee {id} stopped session!")
                return JsonResponse({'status': 'success', 'session_id': session.id})
            except Employee.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Employee not found'})
            except WorkSession.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Active session not found'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def index(request):
    return render(request, 'index.html')

