from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from apps.account.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=60, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=60, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({'success': True, 'message': 'Password did not match, please try again'})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=101, required=True)
    password = serializers.CharField(max_length=68, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, obj):
        user = User.objects.filter(email=obj.get('email')).first()
        return user.token

    class Meta:
        model = User
        fields = ('email', 'password', 'token')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed({
                'message': 'Invalid email or password'
            })
        if not user.is_active:
            raise AuthenticationFailed({'message': 'Account disabled'})

        data = {
            'success': True,
            'email': user.email,
            'token': user.token,
        }
        return data


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=505)

    class Meta:
        model = User
        fields = ('token', )


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('email', )


class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=66, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=66, write_only=True)
    uidb64 = serializers.CharField(max_length=69, required=True)
    token = serializers.CharField(max_length=505, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2', 'uidb64', 'token')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')
        _id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.filter(id=_id).first()
        if not PasswordResetTokenGenerator.check_token(user, token):
            raise AuthenticationFailed({'success': False, 'message': 'The token is not valid'})
        if password != password2:
            raise serializers.ValidationError({
                'success': False, 'message': 'Password did not match, please try again'
            })
        user.set_password(password)
        user.save()
        return user


class ChangeNewPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(min_length=6, max_length=64, write_only=True)
    password = serializers.CharField(min_length=6, max_length=64, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=64, write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'password' 'password2')

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError({
                'success': False, 'message': 'Old password did not match, please try again'
            })
        if password != password2:
            raise serializers.ValidationError({
                'success': False, 'message': 'Password did not match, please try again'
            })
        user.set_password(password)
        user.save()
        return attrs

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'bio',
            'image',
            )