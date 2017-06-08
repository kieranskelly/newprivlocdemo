__author__ = 'cory1'
from google.appengine.api import mail


class LandingZoneEmailHandler:

    def __init__(self):
        self.recipients = ["3129271999@vtext.com",
                           "2026078807@vtext.com",
                           "4152971226@txt.att.net"]
        self.sender_address = "Aerwaze <corylstewart@gmail.com>"

    def send_alert(self, body, subject='Airspace Alerts'):
        for recipient in self.recipients:
            mail.send_mail(self.sender_address, recipient, subject, body)
