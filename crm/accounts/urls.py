from django.urls import path
from .views import signup,create_employee,login

urlpatterns = [
    path("signup/",create_employee,name="signup"),
    path("login/",login,name="login")
]
    
    