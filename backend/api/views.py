from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from links.models import Link
from .serializers import LinkSerializer
import json
from users.models import customUser
from django.conf import settings

@api_view(['POST'])
def create_short_link(request):
    json_data=json.loads(request.body)
    if "original_url" in json_data:
        original_url=request.data['original_url']
        user_active=None
        if 'user' in json_data:
            user=request.data['user']
            try:
                user_active=customUser.objects.get(id=user)
            except:
                user_active=None
    try:
        link_exist=Link.objects.get(original_url=original_url)
        if user_active is not None:
            link_exist.user.add(user_active)
            link_exist.save()
        return Response({'short_code': settings.BASE_URL+"/"+link_exist.short_code}, status=status.HTTP_200_OK)
    except:
        serializer = LinkSerializer(data=request.data)
        if serializer.is_valid():
            link = serializer.save()
            return Response({'short_code': settings.BASE_URL+"/"+link.short_code}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def redirect_to_original_url(request, short_code):
    link = Link.objects.get(short_code=short_code)
    link.hits += 1
    link.save()
    return redirect(link.original_url)