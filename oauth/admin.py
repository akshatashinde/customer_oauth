from django.contrib import admin
from oauth.models import Customer,BaseUser


admin.site.register(BaseUser)
admin.site.register(Customer)