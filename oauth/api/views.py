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
    UserLoginSerializer

	)

class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')

@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)
        
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
                # 'is_email_verifird' : user_data['is_email_verified'],


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

class Login(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    # def token (self,request, *args, **kwargs):
    #     data = ' curl -X POST -d "email=admin@gmail.com&password=admin123 http://127.0.0.1:8000/api/auth/token/'
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
                # data.update(myView(email, password))
                return Response(data)
            else:
                return Response({'error': True, 'result': 'This user is not active'})
        else:
            return Response({'error': True, 'result': 'Invalid email or password'})


               


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