from django.shortcuts import render
from rest_framework import generics
from api.serializers import CustomUserSerializer
from .models import customUser
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404
# Create your views here.
class UserCreateView(generics.CreateAPIView):
    queryset = customUser.objects.all()
    serializer_class = CustomUserSerializer

def activate_user(request, user_id):
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404('User does not exist.')

    if user.is_active:
        messages.info(request, 'User is already activated.')
    else:
        user.is_active = True
        user.save()
        messages.success(request, 'User activated successfully.')
    return redirect('http://127.0.0.1:8000')