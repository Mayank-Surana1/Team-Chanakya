from twilio.rest import Client

account_sid = 'AC0d87c1e8e4c88f8d1115022ca2b49a98'
auth_token = '6d5ecbc8918f46779cba20c13a720a38'
twilio_number = '+12293540902'

contacts = {
    "John": "+917019805605"
}

import geocoder
lat = 0
lon = 0
g = geocoder.ip('me')
if g.ok:
    lat = g.latlng[0]
    lon = g.latlng[1]
else:
    print("Unable to get location")
    exit(0)
# Predefined SOS message
sos_message = f"This is an SOS alert Send HELP at {lat, lon}"

# Function to send SOS to contacts
def send_sos_to_contacts():
    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    for name, phone_number in contacts.items():
        message = client.messages.create(
            body=sos_message,
            from_=twilio_number,  # Twilio phone number
            to=phone_number
        )
        print(f"SOS sent to {name} at {phone_number}: {message.sid}")

send_sos_to_contacts()