from django.core import mail
import random
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import base64

def sendVerificationEmail(user, email):
    verification_code = str(random.randint(0, 999999))
    while len(verification_code) < 6:
        verification_code = "0" + verification_code
    email_base64_bytes = base64.b64encode(email.encode("ascii"))
    email_base64 = email_base64_bytes.decode("ascii")
    verification_code = f"{email_base64}{verification_code}"
    html_message = render_to_string('email_form.html', {'verification_code': verification_code})
    plain_message = f"Mã xác thực của bạn: {verification_code}"
    mail.send_mail(
        subject="Verification code",
        from_email='Schat <schatemail.system@gmail.com>',
        message=plain_message,
        recipient_list=[email],
        html_message=html_message
    )
    userProfile = user.profile
    userProfile.verification_code = verification_code
    userProfile.save()


def resendVerificationEmail(user, email):
    if user.profile.verified: return False
    user.email = email
    user.save()
    verification_code = sendVerificationEmail(user, email)
    return True

def sendForgetPasswordEmail(reset_password_token):
    user = reset_password_token.user
    forget_password_token = "{}".format(reset_password_token.key)
    
    greetings = "Hi {}!".format(reset_password_token.user.username)
    email_html_content = "<html><body><p>{greetings}</p> \
                        <p>Please use this Token for password Reset on SChat website: <b>{token}</b></p></body></html>".format(
                            greetings=greetings,
                            token=forget_password_token
                        )

    mail.send_mail(
        subject="Forget Password Token",
        from_email='Schat <schatemail.system@gmail.com>',
        message=greetings,
        recipient_list=[user.email],
        html_message=email_html_content
    )