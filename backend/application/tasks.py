from celery import shared_task 
import csv
import os
from jinja2 import Template
from .mail import send_email
from .models import User, UserCardDetail
import datetime
import requests
import time
import socket

def is_broker_available(host="localhost", port=6379, timeout=0.2):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        available = (s.connect_ex((host, port)) == 0)
        s.close()
        return available
    except Exception:
        return False

# task 1 - Download CSV report for user.
# User(client) triggered async job 
@shared_task(ignore_results = False, name = "download_csv_report")
def csv_report():
    card_details = UserCardDetail.query.all() # card details
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file_name = f"card_{timestamp}.csv"
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    os.makedirs(static_dir, exist_ok = True)
    filepath = os.path.join(static_dir, csv_file_name)
    with open(filepath, 'w', newline = "") as csvfile:
        sr_no = 1
        card_csv = csv.writer(csvfile, delimiter = ',')
        card_csv.writerow(['Sr No.', 'Attribute Name', 'Attribute Value', 'Card Name', 'User ID'])
        for c in card_details:
            this_card = [sr_no, c.attr_name, c.attr_val, c.cardname, c.user_id]
            card_csv.writerow(this_card)
            sr_no += 1
    time.sleep(2) # brief sleep to demonstrate async processing
    return csv_file_name


# task 2 - Monthly report sent via mail 
# scheduled job via crontab 
@shared_task(ignore_results = False, name = "monthly_report")
def monthly_report():
    users = User.query.filter_by(role = "user").all()
    for user in users:
        user_data = {}
        user_data['username'] = user.username
        user_data['email'] = user.email
        details = []
        card_details = UserCardDetail.query.filter_by(attr_name = "status", user_id = user.id)
        for info in card_details:
            info_dict = {}
            info_dict["cardname"] = info.cardname
            info_dict["status"] = info.attr_val
            details.append(info_dict)
        user_data['details'] = details 
        # till this point you get user data in list of dict form
        mail_template = """
        <h3>Dear {{user_data.username}}</h3>
        <p>Please find the current status of your cards in the table below.</p>
        <p>Visit our ecard app at http://127.0.0.1:5173 for details.</p>
        <table border="1" cellpadding="5">
            <tr>
                <th>Card Name</th>
                <th>Status</th>
            </tr>
            {% for detail in user_data.details %}
            <tr>
                <td>{{detail.cardname}}</td>
                <td>{{detail.status}}</td>
            </tr>
            {% endfor %}
        </table>
        <h5>Regards<br>
        E card V2<br>
        IITM BS Degree</h5>
        """
        message = Template(mail_template).render(user_data = user_data)
        # the data is then rendered into a mail body
        try:
            send_email(user.email, subject = "Monthly card detail Report - E card", message = message)
        except Exception as e:
            print(f"[Celery Monthly Report] Could not send email to {user.email}: {e}")
    return "Monthly reports sent" 

# task 3 - Card generation update sent via G-chat webhook
# Backend(endpoint) triggered async job
@shared_task(ignore_results = False, name = "generate_msg")
def generate_msg(username, cardname):
    text = f"Hi {username}, your {cardname} card has been generated. Please check the app at http://127.0.0.1:5173"
    try:
        response = requests.post(
            "https://chat.googleapis.com/v1/spaces/AAQAiW6yfws/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=2y5k4hP3lazOpksDAyPPxsCL2sbrLz5J0v44rCWRZ14",
            json = {"text": text},
            timeout = 5
        )
        print("Webhook response:", response.status_code)
    except Exception as e:
        print("[Celery generate_msg] Webhook notice skipped or failed:", e)
    return "The delivery is sent to user"
