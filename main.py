import requests
from datetime import datetime
import smtplib
import time

email = "testhuman00001@gmail.com"
password = "random_letters"

MY_LAT = coord_1
MY_LONG = coord_2


def in_range():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    distance_from_lat = MY_LAT - iss_latitude
    distance_from_lng = MY_LONG - iss_longitude
    if 5 >= distance_from_lat >= -5 and 5 >= distance_from_lng >= -5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "timezone": "CST"

    }

    response = requests.get("https://api.sunrisesunset.io/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split(":")[0])
    sunset = int(data["results"]["sunset"].split(":")[0])
    print(data)
    print(sunrise)
    print(sunset)
    time_now = datetime.now()
    print(time_now)
    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True

cycle = 0
while True:
    cycle += 1
    print(cycle)
    if in_range() and is_night():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(email, password=password)
            connection.sendmail(from_addr=email, to_addrs="recipient@gmail.com",
                                msg="Subject: Look UP\n\nThe ISS is above you in the sky")
        print("Email Sent")
    time.sleep(60)
