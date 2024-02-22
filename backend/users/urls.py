from django.urls import path
from .views import UserCreateView,activate_user
urlpatterns = [
    path('register/',UserCreateView.as_view(), name='register'),
    path('activate/<str:user_id>/',activate_user,name='activate'),
]
