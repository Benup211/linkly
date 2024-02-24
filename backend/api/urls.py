from django.urls import path
from .views import create_short_link, redirect_to_original_url,getUserLinks

urlpatterns = [
    # Other URL patterns
    path('short-links/', create_short_link, name='create_short_link'),
    path('<str:short_code>/', redirect_to_original_url, name='redirect_to_original_url'),
    path('user/links/',getUserLinks,name="user_links"),
]