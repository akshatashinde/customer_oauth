from django.conf import settings

from django.db.models import Q
from rest_framework import serializers
from oauth.models import BaseUser
from rest_framework.serializers import (
	EmailField,
	CharField,
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField,
	ValidationError,

	)

class UserSerializer(ModelSerializer):
    """
    Serializer for registering new users.
    This class excepts users details validates them
    and returns user object.
    """
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    phone_number = serializers.CharField(max_length=15)
    class Meta:
        model = BaseUser
        fields = [
            'id',
            'email',
            'phone_number',
            # 'get_date_joined',
            'get_is_email_verified',
            'password',
            'confirm_password'
            ]

        read_only_fields = ('id', 'password', 'confirm_password')

    def create(self, validated_data):
        # first_name = validated_data.get('first_name', '')
        phone_number = validated_data.get('phone_number', '')
        user = BaseUser.objects.create(
                email=validated_data['email'],
                phone_number = phone_number,
                is_active=True,
                is_staff = True,
                is_email_verified=True

        )

        user.set_password(validated_data['password'])
        user.save()

        return user



class UserLoginSerializer(ModelSerializer):
	email = EmailField(label='Email Address',allow_blank=True, required=False)
	password = CharField(allow_blank=True, required=False)
	token = CharField(allow_blank=True, read_only=True)
	class Meta:
		model = BaseUser
		fields =[
			'email', 
			'password',	
			'get_phone_number',
			'date_joined',
			'get_is_email_verified',
			'token'
		]
		extra_kwargs = {"password":
							{"write_only":True}

							}

	def validate(self, data):
		user_obj =None
		email = data.get("email",None)
		password = data["password"]
		if not email :
			raise ValidationError("This email is required to login.")

		user = BaseUser.objects.filter(
				Q(email=email)
			).distinct()
		# user = user.exclude(email_isnull=True).exclude(email_iexact='')
		if user.exists() and user.count() ==1:
			user_obj = user.first()
		else:
			raise ValidationError("This username/email is not valid.")

		if user_obj:
			if not user_obj.check_password(password):
				raise ValidationError("Incorrect credentials please try again.")

		data["token"] = "SOME RANDOM TOKEN"		
		return data	 	


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('username', 'password')
        write_only_fields = ('password',)



# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=False, allow_blank=True)
#     email = serializers.EmailField(required=False, allow_blank=True)
#     password = serializers.CharField(style={'input_type': 'password'})

#     def _validate_email(self, email, password):
#         user = None

#         if email and password:
#             user = authenticate(email=email, password=password)
#         else:
#             msg = _('Must include "email" and "password".')
#             raise exceptions.ValidationError(msg)

#         return user

#     def _validate_username(self, username, password):
#         user = None

#         if username and password:
#             user = authenticate(username=username, password=password)
#         else:
#             msg = _('Must include "username" and "password".')
#             raise exceptions.ValidationError(msg)

#         return user

#     def _validate_username_email(self, username, email, password):
#         user = None

#         if email and password:
#             user = authenticate(email=email, password=password)
#         elif username and password:
#             user = authenticate(username=username, password=password)
#         else:
#             msg = _('Must include either "username" or "email" and "password".')
#             raise exceptions.ValidationError(msg)

#         return user

#     def validate(self, attrs):
#         username = attrs.get('username')
#         email = attrs.get('email')
#         password = attrs.get('password')

#         user = None

#         if 'allauth' in settings.INSTALLED_APPS:
#             from allauth.account import app_settings

#             # Authentication through email
#             if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
#                 user = self._validate_email(email, password)

#             # Authentication through username
#             if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
#                 user = self._validate_username(username, password)

#             # Authentication through either username or email
#             else:
#                 user = self._validate_username_email(username, email, password)

#         else:
#             # Authentication without using allauth
#             if email:
#                 try:
#                     username = UserModel.objects.get(email__iexact=email).get_username()
#                 except UserModel.DoesNotExist:
#                     pass

#             if username:
#                 user = self._validate_username_email(username, '', password)

#         # Did we get back an active user?
#         if user:
#             if not user.is_active:
#                 msg = _('User account is disabled.')
#                 raise exceptions.ValidationError(msg)
#         else:
#             msg = _('Unable to log in with provided credentials.')
#             raise exceptions.ValidationError(msg)

#         # If required, is the email verified?
#         if 'rest_auth.registration' in settings.INSTALLED_APPS:
#             from allauth.account import app_settings
#             if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
#                 email_address = user.emailaddress_set.get(email=user.email)
#                 if not email_address.verified:
#                     raise serializers.ValidationError(_('E-mail is not verified.'))

#         attrs['user'] = user
#         return attrs    


