from handlers.edit_location_handler import EnhancedHandler
from google.appengine.ext import ndb

#import sys
#print sys.path

import twilio
from twilio.rest import Client

class PermitCreater(EnhancedHandler):

    def get(self):
        if not self.confirm_user_logged_in():
            return
        self.add_page_name('permit_maker')
        self.render('permit_maker.html', **self.arg_dict)

    def post(self):
        self.zone_city = self.request.get('zone_city')
        self.zone_name = self.request.get('zone_name')
        # can only add a city!!
        print self.zone_city, self.zone_name
        PermitZone.add_new_permit_zone(name=self.zone_name,
                                       city=self.zone_city)

class PermitApplication(EnhancedHandler):
    print 'PermitApplication init'

    def get(self, zone='atherton'):
        #self.response.write('This is the ProductHandler. '
        #    'The product id is %s' % zone)
        self.render('permits/%s.html' %zone)

    def post(self):
        response = self.request.POST
        print 'rsponse', response.items()

        self.render('permit_applied.html')

class PermitZone(ndb.Model):
    id = ndb.StringProperty() #"1001"
    name = ndb.StringProperty() #"Holbrook-Palmer Park"
    city = ndb.StringProperty() #"Atherton"
    location = ndb.GeoPtProperty()
    #type = ndb.

    @staticmethod
    def add_new_permit_zone(name, city):
        new_zone = PermitZone(name=name,
                              city=city)
        return new_zone.put()


    @staticmethod
    def get_by_id(id):
        return PermitZone.query(PermitZone.id == id)

    @staticmethod
    def get_by_city(city):
        return PermitZone.query(PermitZone.city == city)


class PermitApplier(EnhancedHandler):

    def get(self, zone=None):
        #if not self.confirm_user_logged_in():
        #    return
        self.add_page_name('permit_applier')
        self.render('permit_applier.html', **self.arg_dict)

    # /submit button automatically sends a post request to the webpage
    def post(self):
        self.phone_number = self.request.get('phone_number')
        self.zone_city = self.request.get('zone_city')
        print 'user entered phone number:', self.phone_number
        print self.zone_city

        # check the database to see if the entry is valid. (it should always be because the form draws from the same place.
        # hwo to aritecture?
        response = PermitZone.get_by_city(self.zone_city).fetch()
        # need to parse


        # generate the link to send to the user
        link = self.generateLink(self.zone_city)

        # send SMS to User
        self.send_sms(self.phone_number, link)

        self.response.write('Thank you for your request. You should receive a text message with a link to the permit application.')

        #self.render('permit_applied.html', **self.arg_dict)

    def generateLink(self, city):
        link = 'wired-strategy-174203.appspot.com/permit_apply/'+city.__str__()
        return link

    def send_sms(self, phone_number, link):
        # from twilio
        account_sid = "ACd686b67138bbee502e1d705fb3bcd19f"
        auth_token  = "f4ba6887175a913e6631af950e520299"
        twilio_phone_number = "+18324301720"

        client = Client(account_sid, auth_token)

        client.messages.create(
            to=phone_number,
            from_=twilio_phone_number.__str__(),
            body="Welcome to Aerwaze! Tap the link to apply for the permit. "+link,
            )


class PermitReviewer(EnhancedHandler):
    def get(self):
        pass