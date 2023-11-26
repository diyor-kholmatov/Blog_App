from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, ResetPasswordSerializer, \
    SetNewPasswordSerializer, ChangeNewPasswordSerializer, AccountSerializer
from rest_framework import generics, views, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrReadOnlyForAccount, IsAdminUserForAccount
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from drf_yasg import openapi
from apps.account.models import User
from .utils import Util
import jwt


class AccountRegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer


    # create user
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user)

        current_site = 'localhost:8000/'
        relative_link = 'account/verify-email'
        ads_url = f'http://{current_site}{relative_link}?token={str(token.access_token)}'
        email_body = (f'Hi, {user.email} \n'
                      f'Use link below to activate your email\n'
                      f'{ads_url}')
        data = {
            'to_email': user.email,
            'email_subject': 'Activate email to BAN',
            'email_body': email_body
        }
        Util.send_email(data)

        return Response({'success': True, 'message': 'Activate url was sent your email'},
                        status=status.HTTP_201_CREATED)


class EmailVerificationAPIView(APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes =  (AllowAny,)
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Verify email',
                                           type=openapi.TYPE_STRING)

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['H5256'])
            user_id = User.odjects.get(id=payload['user_id'])
            if not user_id.is_active:
                user_id.is_active = True
                user_id.save()
            return Response({'success': True, 'message': 'Email successfuly activate'},
                            status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as e:
            return Response({'success': False, 'message': f'Verification expired Invalid token | {e.args}'},
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({'success': False, 'message': f'Invalid token | {e.args}'},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({'success': True, 'data': serializer.data},
                             status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Credentials is not valid'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = User.objects.filter(email=request.data['email']).first()

        if user:
            uidb64 =urlsafe_base64_decode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = 'localhost:8000/'
            abs_url = f'http://{current_site}account/set-password-confirm/?uidb64={uidb64}&token={token}'
            email_body = f'Hello, \n User link below to activate your email \n {abs_url}'
            data = {
                'to_email': user.email,
                'email_subject': 'Reset password',
                'email_body': email_body
            }
            Util.send_email(data)
            return Response({'success': True, 'message': 'Link sent to email'}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Email did not match'}, status=status.HTTP_400_BAD_REQUEST)


class SetPasswordConfirmAPIView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):
        try:
            id = smart_bytes(urlsafe_base64_decode(uidb64))
            user = User.odjects.filter(id=id).first()
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'success': False, 'message': 'Token is not valid, please try again'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        except DjangoUnicodeDecodeError as e:
            return Response({'success': False, 'message': f'DecodeError: {e.args}'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response({'success': True, 'message': 'Successfully checked', 'uidb64': uidb64, 'token': token},
                        status=status.HTTP_200_OK)

class SetNewPasswordCompletedAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = (AllowAny,)

    def parch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({'success': True, 'message': 'Successfully set new password'},
                            status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Credentials is invalid'},
                         status=status.HTTP_406_NOT_ACCEPTABLE)


class ChangePasswordCompletedAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ChangeNewPasswordSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Successfully set new password'},
                        status=status.HTTP_200_OK)

class MyAccountAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyForAccount)
    lookup_field = 'email'


