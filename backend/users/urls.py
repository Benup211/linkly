from django.urls import path
from .views import UserCreateView,activate_user,LoginView
urlpatterns = [
    path('register/',UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/<str:user_id>/',activate_user,name='activate'),
]
