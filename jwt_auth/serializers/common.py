from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.pop('password', None)
        password_confirmation = data.pop('password_confirmation', None)

        # Check if email is provided
        email = data.get('email', None)
        if not email:
            raise serializers.ValidationError(
                {'email': 'This field is required'})

        # Check if password is provided
        if not password:
            raise serializers.ValidationError(
                {'password': 'This field is required'})

        # Check if password confirmation is provided
        if not password_confirmation:
            raise serializers.ValidationError(
                {'password_confirmation': 'This field is required'})

        if password and password_confirmation:
            if password != password_confirmation:
                raise serializers.ValidationError(
                    {'password_confirmation': 'Passwords do not match'})
            try:
                password_validation.validate_password(password)
            except ValidationError as err:
                # Django's ValidationError would surface as a 500; report it as a field error.
                raise serializers.ValidationError({'password': list(err.messages)})
            data['password'] = make_password(password)
        return data

    class Meta:
        model = User
        fields = ('id', 'email', 'description', 'profile_image',
                  'username', 'discord_username', 'password', 'password_confirmation',
                  'date_joined')
