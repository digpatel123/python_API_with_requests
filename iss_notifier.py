import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText


def send_email(subject, message):
    sender_email = "your_email@example.com"
    receiver_email = "recipient_email@example.com"
    smtp_server = "smtp.example.com"
    smtp_port = 587
    username = "your_username"
    password = "your_password"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)


def get_sunrise_sunset(latitude, longitude):
    url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&formatted=0"
    response = requests.get(url)
    data = response.json()

    sunrise = data['results']['sunrise']
    sunset = data['results']['sunset']

    return sunrise, sunset


def get_iss_location():
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    data = response.json()

    latitude = float(data['iss_position']['latitude'])
    longitude = float(data['iss_position']['longitude'])

    return latitude, longitude


# Latitude and Longitude of London
latitude = 51.5074
longitude = -0.1278

sunrise_time, sunset_time = get_sunrise_sunset(latitude, longitude)

# Get the current time
current_time = datetime.now().strftime("%H")
print(current_time)


def nighttime():
    # Compare the unformatted sunrise and sunset times with the current time
    if current_time <= sunrise_time or current_time >= sunset_time:
        return True
    else:
        return False


def iss_is_close():
    iss_latitude, iss_longitude = get_iss_location()

    # Calculate the distance between London and the ISS
    distance_lat = abs(latitude - iss_latitude)
    distance_lon = abs(longitude - iss_longitude)

    # Check if the ISS is close to London (within 5 degrees)
    if distance_lat or distance_lon <= 5:
        return True


if iss_is_close() and nighttime():
    # Send an email
    subject = "ISS Alert"
    message = "The International Space Station is close to London during nighttime."
    send_email(subject, message)
    print("Email sent!")

print("Sunrise time:", sunrise_time)
print("Sunset time:", sunset_time)
print("Current time:", current_time)
