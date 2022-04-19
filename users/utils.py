from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
import base64
import os
from twilio.rest import Client


def generate_key(phone):
    key = str(phone) + str(datetime.date(datetime.now())) + "aajatujhechandparlechalue"
    print("Test Key ", key)
    return base64.b32encode(key.encode())

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def send_otp(phone, otp):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Your OTP is " + str(otp),
        from_= '+15716217575',
        to=phone
    )

    print(message.sid)

