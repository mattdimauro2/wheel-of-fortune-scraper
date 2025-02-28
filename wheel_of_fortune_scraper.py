# Wheel of Fortune Spin ID Tracker
import os
import csv
import requests
from bs4 import BeautifulSoup
import time
import schedule
import smtplib
from email.message import EmailMessage
from datetime import datetime

#1.) Hard-coded dictionary of all user spin ID's and emails to track. Format of the dictionary is {Spin ID: email address}
tracked_spin_ids = {"MD3163259": "mattdimauro2@gmail.com"}

#2.) Email credentials for sending out the winning notification email. My email password is saved in my OS (using an app password from gmail for Python).
EMAIL_ADDRESS = "mattdimauro2@gmail.com"
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")
if not EMAIL_PASSWORD:
    raise ValueError("Email password has not yet been set in os environment.")

#3.) CSV log file for historical winners
winning_historical_file = "winning_spin_id_log1.csv"

#4.) Scrape the winning spin id using requests and beautiful soup to parse the html.
def get_winning_spin_id():
    url = "http://www.wheeloffortunesolutions.com/spinid.html"
    response = requests.get(url)
    if response.status_code != 200:   #will stop the process if the website is not reachable.
        print("The page is currently not reachable")
        return
    soup = BeautifulSoup(response.text, features="html.parser")
    spin_id_section = soup.find(name="td", class_="TableSpinID")    #section of html where the winning spin id is located
    return spin_id_section.text.strip() if spin_id_section else None

#5.) Send an email to the winner if there is one in our dictionary.
def send_winner_email(recipient, winning_spin_id):
    message = EmailMessage()
    message["Subject"] = 'YOU ARE THE WINNING WHEEL OF FORTUNE SPIN ID!'
    message["From"] = EMAIL_ADDRESS
    message["To"] = recipient
    message.set_content(f"Congrats! Your Spin ID {winning_spin_id} won tonight’s Wheel of Fortune $10K prize!!! Claim it at wheeloffortune.com within 24 hours!")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)
        print(f"Email has been successfully sent to {recipient}")
    except Exception as e:
        print(f"Email could not be sent to {recipient} because of: {e}")

#6.) Log the winning spin ID and date to a CSV for historical tracking purposes.
def log_winning_spin_id(winning_spin_id):
    file_exists = os.path.isfile(winning_historical_file)

    with open(winning_historical_file, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Winning Spin ID"])
        log_entry = winning_spin_id if winning_spin_id else "No winner tonight"    #This will record "No winner tonight" in the CSV if the website doesn't document a winner
        writer.writerow([datetime.now().strftime("%m-%d-%Y"), log_entry])

#7.) Check the winning Spin ID and initiate the functions to log the winning id and send an email if there is a winner in our dictionary.
def check_spin_id():
    if datetime.today().weekday() >= 5:
        print("Skipping the check today as it is a weekend and there is no Wheel of Fortune tonight.")
        return

    print("Checking the winning Spin ID tonight...")
    winning_spin_id = get_winning_spin_id()

    if winning_spin_id:
        print(f"{datetime.now().strftime("%m-%d-%Y")} winning Spin ID: {winning_spin_id}")
    else:
        print(f"{datetime.now().strftime("%m-%d-%Y")} No winner found")
    log_winning_spin_id(winning_spin_id)

    if winning_spin_id in tracked_spin_ids:
        send_winner_email(tracked_spin_ids[winning_spin_id], winning_spin_id)
    else:
        print("No tracked spin ID won today")

#8.) Schedule the script to run every weeknight at 10pm EST
schedule.every().monday.at("22:00").do(check_spin_id)
schedule.every().tuesday.at("22:00").do(check_spin_id)
schedule.every().wednesday.at("22:00").do(check_spin_id)
schedule.every().thursday.at("22:00").do(check_spin_id)
schedule.every().friday.at("22:00").do(check_spin_id)

# Keep the script running
if __name__ == "__main__":
    print("Starting Wheel of Fortune tracker...")
    check_spin_id()
    while True:
        schedule.run_pending()
        time.sleep(60)
