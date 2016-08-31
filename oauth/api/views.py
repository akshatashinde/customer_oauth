import requests 
import json


from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.contrib.auth import authenticate, login, logout

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from django.template.loader import get_template
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_205_RESET_CONTENT
#from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework import generics
from permissions import IsAuthenticatedOrCreate

from cc import helper, error_conf
from oauth import system_error
from oauth import utils

from oauthlib.common import generate_token

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )

from oauth.models import BaseUser,Customer
from .serializers import (
	UserSerializer,
    UserLoginSerializer,
    SignUpSerializer

	)


class CreateUserView1(APIView):
    """
    Creating API for User creation which takes user
    details(email, password, confirm_password, first_name
    last_name, phone_number) as input validates the user details and
    creates a user account.
    """
    model = BaseUser
    serializer_class = UserSerializer

    def post(self, request):

        user_data = request.data

        error_checks = system_error.check_for_registration_input_error(user_data)
        if error_checks:
            return Response(error_checks,
                            status=status.HTTP_412_PRECONDITION_FAILED)

        # user_data['role'] = "Normal User"
        serializer = UserSerializer(data=user_data)

        if serializer.is_valid():
            user = serializer.save()

            """
            Creating social Details with provider name
            as Audecampus and provider_id as user_id
            """
            # helper.add_social_details(user, 'Audecampus', user.id)

            """
            This generates the OTP for the registered email
            and send the OTP to the users email.
            """
            # validated_otp_num = utils.opt_generator(user)

            # utils.send_opt_to_mail(user_data, validated_otp_num, user)

            token = helper.generate_oauth_token(
                self, user.email,
                user_data.get('confirm_password'))

            if token.status_code != 200:
                return Response({'msg': 'Username or password is incorrect'},
                                status=status.HTTP_412_PRECONDITION_FAILED)

            return Response({
                'success': True,
                'msg': 'Registration Successfully.',
                'Email' : user_data['email'],
                'Mobile No' : user_data['phone_number'],
                'token': json.loads(token._content)})

        return Response(error_conf.GENERIC_API_FALIURE,
                        status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    """
    Creating API for User Authentication
    Based On roles and UserName and Passwords

    Note:-
    Checks whether the request is from audecampus user
    by checking the provider name in UserSocialDetails
    Table and if that entry is primary.
    """

    def post(self, request, format=None):
        """
        Return a Valid token if username and password
        is valid for a given client
        """

        if request.data:
            data = request.data

            error_checks = system_error.check_for_login_input_error(data)

            if (error_checks and error_checks.get('error_code') != 7):
                return Response(error_checks,
                                status=status.HTTP_412_PRECONDITION_FAILED)

            email = data.get('email')
            password = data.get('password')
            # source = data.get('source')

            user = BaseUser.objects.get(email=email)
            email = user.email

            print email


            if (user.is_superuser or not user.is_superuser ):

                login_success_data = helper.generate_oauth_token(self, email, password)
                if login_success_data.status_code != 200:
                    return Response(error_conf.INVALID_PASSWORD,
                                    status=status.HTTP_412_PRECONDITION_FAILED)

                responce_dict = json.loads(login_success_data._content)

                if (error_checks and error_checks.get('error_code') == 7):
                    responce_dict['is_email_verified'] = False
                else:
                    responce_dict['is_email_verified'] = True

        

                return HttpResponse(json.dumps(responce_dict),
                                    content_type='application/json')

        return Response(error_conf.NO_INPUT_DATA,
                        status=status.HTTP_400_BAD_REQUEST)



class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')

@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)


def create_token(user):
    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    return token.decode('unicode_escape')

class CreateUserView(CreateAPIView):
    """
    Creating API for User creation which takes user
    details(email, password, confirm_password,
    phone_number) as input validates the user details and
    creates a user account.
    """
    model = BaseUser
    serializer_class = UserSerializer

    def post(self, request):

        user_data = request.data

        serializer = UserSerializer(data=user_data)

        if serializer.is_valid():
            user = serializer.save()
            # user.update(create_token(user.email))
            # token = generate_token(
            #     self, user.email,
            #     user_data.get('password'))

            # if token.status_code != 200:
            #     return Response({'msg': 'Username or password is incorrect'},
            #                     status=status.HTTP_412_PRECONDITION_FAILED)

            return Response({
                'success': True,
                'msg': 'Registration Successfully Please Verify Email',
                'Email' : user_data['email'],
                'Mobile No' : user_data['phone_number'],
                'get_date_joined' : user_data['get_date_joined'],
                'get_is_email_verified' : user_data['get_is_email_verified'],

                # 'token': json.loads(token._content)
                })

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)




class UserLoginAPIView(APIView):
    permission_classes = [AllowAny] 
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer
            return Response(data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)     

def myView(email, password):
        url = "http://127.0.0.1:8000/api/auth/token/"
        # payload = json.load(open("requests.json"))
        headers = {'content-type':'application/json', 'Accept-Charset': 'UTF-8'}
        r = requests.post(url, data=json.dumps({"email" : email,"password": password}), headers=headers)
        # response = urllib.request.urlopen(r)
        data = r.json()
        return data

class Login(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    # def token (self,request, *args, **kwargs):
    #     data = "curl -X POST -d "email=admin@gmail.com&password=admin123 http://127.0.0.1:8000/api/auth/token/" "
    #     headers = {'X-OpenAM-Username':'user', 'X-OpenAM-Password':'password', 'Content-Type':'application/json'}
    #     data = {}
    #     r = requests.get('http://openam.sp.com:8095/openamSP/json/authenticate', headers=headers, params=data)


    def post(self, request, *args, **kwargs):
        user_data = request.data
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                # Correct password, and the user is marked "active"
                login(request, user)
                # Get user details
                user_detail = BaseUser.objects.get(pk=user.id)
                user_serializer = UserLoginSerializer(user_detail)
                # ret data
                data = {'error': False, 'result': user_serializer.data }
                data.update(myView(email, password))
                return Response(data)
            else:
                return Response({'error': True, 'result': 'This user is not active'})
        else:
            return Response({'error': True, 'result': 'Invalid email or password'})


class LogoutView(APIView):
    permission_classes = (AllowAny,)               
    def get(self, request):
        logout(request)
        return Response({"error": False, 'result': "logged out successfully"})


class SignUp(generics.CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)        

# class LoginView(GenericAPIView):

#     """
#     Check the credentials and return the REST Token
#     if the credentials are valid and authenticated.
#     Calls Django Auth login method to register User ID
#     in Django session framework

#     Accept the following POST parameters: username, password
#     Return the REST Framework Token Object's key.
#     """
#     permission_classes = (AllowAny,)
#     serializer_class = LoginSerializer
#     token_model = TokenModel

#     def process_login(self):
#         django_login(self.request, self.user)

#     def get_response_serializer(self):
#         if getattr(settings, 'REST_USE_JWT', False):
#             response_serializer = JWTSerializer
#         else:
#             response_serializer = TokenSerializer
#         return response_serializer

#     def login(self):
#         self.user = self.serializer.validated_data['user']

#         if getattr(settings, 'REST_USE_JWT', False):
#             self.token = jwt_encode(self.user)
#         else:
#             self.token = create_token(self.token_model, self.user, self.serializer)

#         if getattr(settings, 'REST_SESSION_LOGIN', True):
#             self.process_login()

#     def get_response(self):
#         serializer_class = self.get_response_serializer()

#         if getattr(settings, 'REST_USE_JWT', False):
#             data = {
#                 'user': self.user,
#                 'token': self.token
#             }
#             serializer = serializer_class(instance=data, context={'request': self.request})
#         else:
#             serializer = serializer_class(instance=self.token, context={'request': self.request})

#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         self.request = request
#         self.serializer = self.get_serializer(data=self.request.data)
#         self.serializer.is_valid(raise_exception=True)

#         self.login()
#         return self.get_response()
