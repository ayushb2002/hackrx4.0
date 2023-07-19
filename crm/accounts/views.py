from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Manager,Team
from .models import Request
from .serializers import RequestSerializer
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

@api_view(['POST'])
def manager_signup(request):
    name = request.data.get('name')
    position = request.data.get('position')
    phone_number = request.data.get('phone_number')
    email = request.data.get('email')

    employee = Employee.objects.create(name=name, position=position, phone_number=phone_number, email=email)
    manager = Manager.objects.create(name=name, employee=employee)

    return Response({'message': 'Manager signup successful'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def sales_employee_signup(request):
    name = request.data.get('name')
    position = request.data.get('position')
    phone_number = request.data.get('phone_number')
    email = request.data.get('email')

    employee = Employee.objects.create(name=name, position=position, phone_number=phone_number, email=email)
    team_name = request.data.get('team_name')
    team = Team.objects.get(name=team_name)
    Request.objects.create(employee=employee)

    return Response({'message': 'Sales employee signup request submitted'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def approve_signup_request(request):
    request_id = request.data.get('request_id')
    request = Request.objects.get(id=request_id)
    request.employee.is_approved = True
    request.employee.save()

    request.delete()

    return Response({'message': 'Signup request approved'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_pending_requests(request):
    pending_requests = Request.objects.filter(is_approved=False)
    serializer = RequestSerializer(pending_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def signup(request):
    return render(request, 'signup.html')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Employee, Manager
from django.db import IntegrityError

def create_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)
        
        # Check if a user with the same email already exists
        if User.objects.filter(email=email).exists():
            error_message = "User with this email already exists"
            return render(request, 'signup.html', {'error_message': error_message})
        try:
            user = User.objects.create_user(username=email,email=email,password=password)
        except IntegrityError:
            error_message = "User creation failed. Please try again."
            return render(request, 'signup.html', {'error_message': error_message})
        # Hash the password
        hashed_password = make_password(password)
        
        # Create the user account
      
        
        # Create the employee account
        try:
            employee = Employee.objects.create(user=user, name=name, position=position, phone_number=phone_number, email=email)
        except IntegrityError:
            # Delete the previously created user
            user.delete()
            error_message = "Employee creation failed. Please try again."
            return render(request, 'signup.html', {'error_message': error_message})
        
        if position == 'manager':
            # Create the manager account if the position is manager
            manager = Manager.objects.create(name=name, employee=employee)
            manager.save()
            employee.is_approved = True
            employee.save()
        
        return redirect('login')  # Replace 'login' with the URL name of your login view
    else:
        return render(request, 'signup.html')  # Replace 'signup.html' with the appropriate template name
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            employee = Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            error_message = "user does not exist"
            return render(request, 'login.html', {'error_message': error_message})
        
        user = authenticate(request, username=email,password=password)  
        employee.user == user
        
        context={
            "username":user,
            "user_type":employee.position,
            "uname":employee.name
        }
        if user is not None:
            auth_login(request, user)
            # return render(request,'dashboard.html',context=context) 
            return redirect("dashboard"+"/?username="+str(user)+"&user_type="+str(employee.position))
        else:
            error_message = "password"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')  