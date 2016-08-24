from django.conf.urls import url, include
from django.contrib.auth.models import User, Group
import oauth2_provider.views as oauth2_views
from django.conf import settings
from .views import (
	ApiEndpoint, secret_page, CreateUserView, UserLoginAPIView, 
	Login, 
	LogoutView,
	)

urlpatterns = [
    # url(r'^hello/', ApiEndpoint, name='endpoint'), # an example resource endpoint
    url(r'^secret/$', secret_page, name='secret'),
    url(r'^register/$', CreateUserView.as_view(),
        name='create_user'),
    url(r'^login1/$', UserLoginAPIView.as_view() , name='login1'),
    url(r'^login/$', Login.as_view() , name='login'),
    url(r'^logout/$',LogoutView.as_view(), name='logout'),
]

