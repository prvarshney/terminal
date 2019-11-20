RECOVER_PASSWORD_SUBJECT = 'Forgot Password OTP'
EMAIL_VERIFICATION_SUBJECT = 'Email Verification OTP'

RECOVER_PASSWORD_BODY = f'''
Hi <user_name>,

Greetings from Team Atom

We have received a request to reset Password for your ATOM account. Use the below OTP to generate new password.

Your OTP (One Time Password) - <otp>


Warm Regards,
Team Atom
'''


EMAIL_VERIFICATION_BODY = f'''
Hi <user_name>,

Greetings from Team Atom

In order to validate your ATOM account, use the OTP given below.

Your OTP (One Time Password) - <otp>


Warm Regards,
Team Atom
'''