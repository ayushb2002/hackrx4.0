from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Manager,Team
from .models import Request
from .serializers import RequestSerializer


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
