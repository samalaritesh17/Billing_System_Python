from twilio.rest import Client

# Twilio credentials
account_sid = ''  # Replace with your Twilio Account SID
auth_token = ''  # Replace with your Twilio Auth Token
from_phone_number = '+'  # Replace with your Twilio phone number

def send_sms(to_phone_number, link):
    try:
        # Create a Twilio client
        client = Client(account_sid, auth_token)

        # Message content
        message_body = ("Dear Customer,\n"
                        "Thank you! for shopping with us.\n"
                        "Please download your E-bill receipt by clicking on the below link.\n"
                        f"You can check the PDF.\nLink: {link}")

        # Send SMS
        message = client.messages.create(
            body=message_body,
            from_=from_phone_number,
            to=to_phone_number
        )

        print(f"Message sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send message: {e}")
































# curl 'https://api.twilio.com/2010-04-01/Accounts/ACd4f2c8c1d8a355f445ce9cd68c8e9216/Messages.json' -X POST \
# --data-urlencode 'To=+916302559136' \
# --data-urlencode 'MessagingServiceSid=MG29376f0ab1594224faaf302ab312868f' \
# --data-urlencode 'Body=Dear Customer,
# Thank you for shopping with us
# Please click on the below link to download your E-bill recipt
# Link : https://billingsystemdata.s3.eu-north-1.amazonaws.com/Bills/bill_15.pdf
# ' \
# -u ACd4f2c8c1d8a355f445ce9cd68c8e9216:[AuthToken]