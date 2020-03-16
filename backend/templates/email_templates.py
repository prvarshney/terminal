EMAIL_RECOVER_PASSWORD_SUBJECT = 'Forgot Password OTP'
EMAIL_VERIFICATION_SUBJECT = 'Email Verification OTP'

EMAIL_RECOVER_PASSWORD_BODY = f'''
Hi <user_name>,

Greetings from Team Terminal

We have received a request to reset Password for your Terminal account. Use the below OTP to generate new password.
This code will be valid for 5 minutes only.

Your OTP (One Time Password) - <otp>


Warm Regards,
Team Terminal
'''


EMAIL_VERIFICATION_BODY = f'''
Hi <user_name>,

Greetings from Team Terminal

In order to validate your Terminal account, use the OTP given below.
This code will be valid for 5 minutes only.

Your OTP (One Time Password) - <otp>


Warm Regards,
Team Terminal
'''