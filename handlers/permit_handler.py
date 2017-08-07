from handlers.edit_location_handler import EnhancedHandler
from google.appengine.ext import ndb
from databases.user import User
from databases.permit import Permit, PermitForm
from databases.location import FlyingLocation
from databases.valid_inputs import ValidInputs
from databases.secure_value import SecureValue
from google.appengine.api import mail
from twilio.rest import Client
import datetime
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

class PermitCreater(EnhancedHandler):
    def get(self):
        # TODO: check for user roles right here. display appropriately
        if not self.confirm_user_logged_in():
            return
        self.arg_dict['type'] = list(Permit.type._choices)
        self.arg_dict['role'] = 'municipality'
        self.add_page_name('permit_maker')
        self.render('permit_maker.html', **self.arg_dict)

    def post(self):
        # TODO: sanitize form input. all values must be present!
        self.type = self.request.get('type')
        self.name = self.request.get('name')
        self.lat = self.request.get('lat')
        self.lon = self.request.get('lon')
        self.cost = self.request.get('cost')
        self.city = self.request.get('city')
        self.end_date = datetime.datetime.strptime(self.request.get('end_date'), '%m/%d/%Y')
        self.start_date = datetime.datetime.strptime(self.request.get('start_date'), '%m/%d/%Y')
        self.user = self.arg_dict['user']

        latlon = '%s, %s' %(self.lat, self.lon)
        print self.user
        user_instance = User.by_user_name(self.user)
        print user_instance

        p = Permit()
        p.owner = user_instance
        p.name = self.name
        p.geo_location = ndb.GeoPt(latlon)
        p.type = self.type
        p.cost = self.cost
        p.city = self.city
        p.start_date = self.start_date
        p.end_date = self.end_date
        k = p.put()

        self.arg_dict['type'] = list(Permit.type._choices)
        self.render('permit_maker.html', **self.arg_dict)

class PermitApplier(EnhancedHandler):
    def get(self):
        permit_id = self.request.get('permit_id')
        phone_number = self.request.get('phone')
        #TODO: janky way of handling none permit_id.
        if not permit_id:
            self.render('/landing_page_form.html')
            return
        permit = Permit.query().filter(Permit.key == ndb.Key('Permit',int(permit_id))).fetch()[0]
        #print 'permit', permit
        #print permit.key.id()
        self.arg_dict['city'] = permit.city
        self.arg_dict['permit_id'] = permit.key.id()
        self.arg_dict['phone_number_placeholder'] = phone_number
        #print self.arg_dict
        self.render('/permits/atherton.html', **self.arg_dict)

    def post(self):
        # if not self.request.get('phone_number'):
        #     self.render('permits/%s.html' %zone)
        #     return
        user_name = self.request.get('email_name')
        password = self.request.get('password_name')
        #password_match = self.request.get('password_match_name')
        phone_number = self.request.get('phone_number')
        uav_make = self.request.get('uav_make')
        uav_model = self.request.get('uav_model')
        description = self.request.get('description')
        permit_id = self.request.get('permit_id')
        date = self.request.get('flight_date')
        city = self.request.get('city')     # TODO: move up to Permit
        flight_date = datetime.datetime.strptime(date, "%Y-%m-%d")

        # TODO: have the permit_id, need to find the Permit entity
        # print 'permit_id', permit_id
        # print ndb.Key('Permit', permit_id).get()
        # print Permit.get_by_id('4600081772707840')
        # p = PermitForm.query(PermitForm.key == permit_ndb_key).fetch()
        # print 'p', p
        # f = PermitForm.query(PermitForm.key == permit_ndb_key).count()
        #
        # print 'f', f

        # if User.phone_number_exists(phone_number):
        #     print 'User exists!'
        #     user = User.by_phone_number(phone_number=phone_number)
        # else:
        #     print 'User does not exist. creating new user.'
        #     user = User() #create_user(user_name=user_name, email=user_email, phone_number=phone_number)
        #     user.user_name = user_name
        #     user.email = user_email
        #     user.phone_number = phone_number

        # if not self.arg_dict['user'] == 'guest':
        #     pass
        # else:
        #     pass
        #
        # if not len(user_name) == 0:
        #     #Check to see that all of the inputs appear to be valid
        #     valid_inputs = ValidInputs()
        #     has_error = False
        #     # if not valid_inputs.valid_user_name(user_name):
        #     #     self.arg_dict['error_user_name'] = "That's not a valid username."
        #     #     has_error = True
        #     if not valid_inputs.valid_password(password):
        #         self.arg_dict['error_password'] = "That wasn't a valid password."
        #         has_error = True
        #     # elif password != password_match:
        #     #     self.arg_dict['error_verify'] = "Your passwords didn't match."
        #     #     has_error = True
        #     if not valid_inputs.valid_email(user_name):
        #         self.arg_dict['error_email'] = "That's not a valid email."
        #         has_error = True
        #     #if there was a bad value re-render the signup page
        #     if has_error:
        #         print has_error, self.arg_dict
        #         self.render('/permits/atherton.html', **self.arg_dict)
        #         return
        #     else:
        #         if User().by_user_name(user_name):
        #             self.arg_dict['error_email'] = "That user already exists."
        #             self.render('/permits/atherton.html', **self.arg_dict)
        #             #print self.arg_dict
        #             return
        #         else:
        #             pw_hash = SecureValue().make_pw_hash(user_name, password)
        #             user = User()#.register_user(user_name, pw_hash, email)
        #             user.user_name = user_name
        #             user.pw_hash = pw_hash
        #             user.phone_number = phone_number
        #             user.put()
        #             self.login(user_name)  # fix this?
        #             #self.redirect('/')
        # else:
        #     user = User.by_user_name(self.arg_dict['user'])


        has_error = False
        user = User().by_user_name(user_name)
        if user:
            secure = SecureValue().check_valid_password(user_name, password, user.pw_hash)
            if not secure:
                self.arg_dict['error_password'] = "Password not valid for user."
                has_error = True

        elif not user:
            pw_hash = SecureValue().make_pw_hash(user_name, password)
            user = User()#.register_user(user_name, pw_hash, email)
            user.user_name = user_name
            user.pw_hash = pw_hash
            user.phone_number = phone_number
            user.put()

        # finish up
        if has_error:
            self.render('/permits/atherton.html', **self.arg_dict)
            return
        else:
            self.login(user.user_name)


        p = PermitForm()
        p.user = user
        #p.permit=permit.key
        p.uav_model=uav_model
        p.uav_make=uav_make
        #p.description=description,
        p.flight_date=flight_date
        # TODO: move up to Permit
        p.city = city
        pn = p.put()

        #print 'permit_app', p
        self.render('permit_applied.html', **self.arg_dict)

    def send_email(self, permit_key):
        #msg = MIMEText(u'<a href="www.google.com">abc</a>','html')
        #msg['Subject'] = "New Permit Application"

        sender_address='permitz@wired-strategy-174203.appspotmail.com'
        to = "Kieran Skelly <kieranskelly@gmail.com>" #Permit.email
        subject ="New Permit Application"
        approve_url = "http://wired-strategy-174203.appspot.com/permit_decision?decision={}&id={}".format('approve',permit_key.urlsafe())
        deny_url = "http://wired-strategy-174203.appspot.com/permit_decision?decision={}&id={}".format('deny', permit_key.urlsafe())
        #user = permit_key.query()
        body = """Dear City:
                Aprove: {}
                Deny: {}""".format(approve_url, deny_url)
        print body
        print approve_url
        mail.send_mail(sender=sender_address,
                   to=to,
                   subject=subject,
                   body=body)

class PermitRequester(EnhancedHandler):
    def get(self):
        # get available permits
        all_permits = Permit.query().fetch()
        tmp = []
        for p in all_permits:
            key = p.key
            city = p.city
            type = p.type
            name = p.name
            id = key.id()
            #if city not in tmp:
            tmp.append([id,city,type,name])

        self.arg_dict['permits'] = tmp

        #print self.arg_dict
        self.add_page_name('permit_requester')
        self.render('permit_requester.html', **self.arg_dict)

    def post(self):
        self.phone_number = self.request.get('phone_number')
        self.permit_id = self.request.get('permit_id')

        # generate the link to send to the user
        link = 'wired-strategy-174203.appspot.com/permit_apply?permit_id={}&phone={}'.format(self.permit_id, self.phone_number)
        #link = 'localhost:8080/permit_apply?permit_id={}&phone={}'.format(self.permit_id, self.phone_number)
        message = "Welcome to Aerwaze! Tap the link to apply for the permit. "+link

        send_sms(self.phone_number, message)

        self.response.write('Thank you for your request. You should receive a text message with a link to the permit application. <br>')
        self.response.write(link)

        #self.render('permit_applied.html', **self.arg_dict)

class PermitReview(EnhancedHandler):
    def get(self):
        permits = PermitForm.query()
        self.arg_dict['permitz'] = {}
        for permit in permits:
            self.permit_to_arg_dict(permit)

        id = self.request.get('permit_id')
        if not id:
            self.render('permit_review.html', **self.arg_dict)
            return

        else:
            user_permit = ''
            for p in permits:
                if id == str(p.key.id()):
                    user_permit = p

        self.render('permit_review.html', **self.arg_dict)

    def permit_to_arg_dict(self, permit):
        #print permit.key.parent() # get parent Permit

        id = permit.key.id()
        self.arg_dict['permitz'][id] = {}
        self.arg_dict['permitz'][id]['id'] = permit.key.id()
        self.arg_dict['permitz'][id]['status'] = permit.status
        self.arg_dict['permitz'][id]['flight_date'] = permit.flight_date
        self.arg_dict['permitz'][id]['name'] = permit.user.user_name
        self.arg_dict['permitz'][id]['uav_model '] = permit.uav_model
        self.arg_dict['permitz'][id]['uav_make'] = permit.uav_make
        self.arg_dict['permitz'][id]['city'] = permit.city


    def post(self):
        decision = self.request.get('decision')
        permit_form_to_change = self.request.get('permit_id')
        print 'permit_review received', decision, permit_form_to_change
        permitforms = PermitForm.query().fetch()
        for pf in permitforms:
            if str(pf.key.id()) == str(permit_form_to_change):
                pf.status = decision
                pf.put()
                self.notify_permit(pf, decision)

    def notify_permit(self,permit_form, decision):
        phone_number = permit_form.user.phone_number
        if decision=="Rejected":
            message = "Your permit has been {}.".format(decision)
        else:
            message = "Your permit has been {}. wired-strategy-174203.appspot.com/preflight".format(decision)
        send_sms(phone_number, message)

class PermitScratch(EnhancedHandler):
    def get(self):
        pass