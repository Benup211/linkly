from rest_framework import generics
from api.serializers import CustomUserSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import customUser
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import status
# Create your views here.
class UserCreateView(generics.CreateAPIView):
    queryset = customUser.objects.all()
    serializer_class = CustomUserSerializer
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        response_data = serializer.create(serializer.validated_data)
        return Response(response_data, status=status.HTTP_200_OK)
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