import logging

from rest_framework import permissions


class IsEmailVerified(permissions.BasePermission):
    """
    Global permission check for User Email Verified or not.
    """

    def has_permission(self, request, view):
        if request.data:
            logging.info(request.data)
        if request.META:
            logging.info(request.META.get('HTTP_AUTHORIZATION'))
        return request.user and request.user.is_email_verified
