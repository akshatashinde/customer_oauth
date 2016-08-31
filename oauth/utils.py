from cc import helper
# from core.models import OTPGenerator

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template


def opt_generator(user):
    prev_otp_obj = OTPGenerator.objects.filter(
        **{'email': user.email})
    if prev_otp_obj.count() > 0:
        [obj.delete() for obj in prev_otp_obj]

    otp_no = helper.generate_otp_number()
    validated_otp_num = helper.validate_otp_number(
        otp_no, user.email)

    OTPGenerator.objects.create(
        otp_number=validated_otp_num,
        email=user.email, is_active=True)

    return validated_otp_num
6

def send_opt_to_mail(user_data, validated_otp_num, user):
    ## Sending Email to User
    subject = "CollegeCampus - Verification"

    html_template = get_template('user_auth/registration_email.html')
    html_context = {}
    html_context['full_name'] = user_data.get('email')
    if user_data.get('full_name'):
        html_context['full_name'] = user_data.get('full_name')
    html_context['passcode'] = validated_otp_num
    html_content = html_template.render(html_context)

    email_to = user.email
    send_mail(subject, None, settings.EMAIL_HOST_USER, [
        email_to, ], html_message=html_content, fail_silently=False)
    ## Sending Email to User FInish
