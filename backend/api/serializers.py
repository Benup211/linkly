from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from links.models import Link
from django.conf import settings

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    def validate_password(self, password):
        try:
            validate_password(password, self.instance)
        except ValidationError as error:
            raise serializers.ValidationError(str(error))
        return password
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User account is not active.')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            pass
        token, _ = Token.objects.get_or_create(user=user)
        return {'token': token.key,'id':user.id}
    
class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['original_url','user']
class UserLinkSerializer(serializers.ModelSerializer):
    short_code = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ['short_code', 'original_url', 'created_at', 'hits']

    def get_short_code(self, obj):
        return settings.BASE_URL + '/' + obj.short_code

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['short_code'] = self.get_short_code(instance)
        return representation