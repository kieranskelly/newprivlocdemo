from handlers.edit_location_handler import EnhancedHandler
from google.appengine.ext import ndb
from databases.user import User
from databases.location import FlyingLocation
from datetime import datetime
from twilio.rest import Client
import logging

def send_sms(phone_number, message):
    # print 'send sms'
    # return
    # from twilio
    account_sid = "ACd686b67138bbee502e1d705fb3bcd19f"
    auth_token  = "f4ba6887175a913e6631af950e520299"
    twilio_phone_number = "+18324301720"

    logging.info('Sending SMS message to {} with content: {}'.format(phone_number, message))

    client = Client(account_sid, auth_token)

    client.messages.create(
        to=phone_number,
        from_=twilio_phone_number.__str__(),
        body=message,
        )
    logging.info('Message sent...')

class PreFlight(EnhancedHandler):
    def get(self):
        self.confirm_user_logged_in()
        if self.arg_dict['user'] == 'guest':
            self.add_page_name('login_page')
            self.render('login_form.html')
        else:
            self.render('preflight.html', **self.arg_dict)

    def post(self):
        lat = self.request.get('lat')
        lon = self.request.get('lon')
        time = datetime.strftime(datetime.now(), "%H:%M:%S") # this should actually be captured on webpage side?
        #date = datetime.strftime(datetime.date(), "%m:%d:%Y")
        #print time
        user = User.query(User.user_name == self.arg_dict['user']).fetch()[0]

        #latlon = '%s, %s' %(lat, lon)

        fl = FlyingLocation()
        fl.user = user
        #fl.geo_location = ndb.GeoPt(latlon)
        fl.lat = lat
        fl.lon = lon
        fl.time = time
        #fl.date = date
        fl.put()

class FlightsHandler(EnhancedHandler):
    def get(self):
        flights = FlyingLocation.query().fetch()
        self.arg_dict['flights'] = {}
        for flight in flights:
            self.flight_to_arg_dict(flight)

        self.render('flights_review.html', **self.arg_dict)

    def flight_to_arg_dict(self, flight):
        key = flight.key.urlsafe()
        print key
        self.arg_dict['flights'][key] = {}
        self.arg_dict['flights'][key]['lat'] = flight.lat
        self.arg_dict['flights'][key]['lon'] = flight.lon
        self.arg_dict['flights'][key]['time'] = flight.time
        self.arg_dict['flights'][key]['name'] = flight.user.user_name
        self.arg_dict['flights'][key]['phone_number '] = flight.user.phone_number

    def post(self):
        p = self.request.get('phone_number')
        [int(pn) for pn in p.split() if pn.isdigit()]
        phone_number = pn.strip('}').strip('u').strip()
        print phone_number
        try:
            send_sms(phone_number=phone_number, message="Alert! Land your drone now!")
        except:
            print 'Error sending sms message.'

class MapHandler(EnhancedHandler):
    def get(self):
        self.render('flights_map.html')
    def post(self):
        pass