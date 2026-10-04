import os
from twilio.rest import Client
# This library reads your .env file
from dotenv import load_dotenv

load_dotenv()

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_num = os.environ.get("TWILIO_PHONE_NUMBER")
user_num = os.environ.get("USER_PHONE_NUMBER")

try:
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        url="http://twilio.com",
        from_=twilio_num,
        to=user_num
    )
    print(f"Success! Call triggered with SID: {call.sid}")
except Exception as e:
    print(f"Error occurred: {e}")
