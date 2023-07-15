from rest_framework import serializers
from .models import Employee, Manager,Team,Request


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
