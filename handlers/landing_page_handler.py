from enhanced_handler import EnhancedHandler
from databases.permit import Permit
from twilio.rest import Client


class LandingPageHandler(EnhancedHandler):
    """Handles requests for the main landing page"""
    def get(self):
        self.arg_dict['role'] = 'municipality'
        #get available permits
        all_permits = Permit.query().fetch()
        tmp = []
        for p in all_permits:
            key = p.key
            city = p.city
            type = p.type
            name = p.name
            id = key.id()
            tmp.append([id,city,type,name])

        self.arg_dict['permits'] = tmp

        print self.arg_dict
        self.add_page_name('landing_page')
        self.render('landing_page_form.html', **self.arg_dict)
    #
    # def post(self):
    #     self.phone_number = self.request.get('phone_number')
    #     self.permit_id = self.request.get('permit_id')
    #
    #     # generate the link to send to the user
    #     link = 'wired-strategy-174203.appspot.com/permit_apply?permit_id={}&phone={}'.format(self.permit_id, self.phone_number)
    #     #link = 'localhost:8080/permit_apply?permit_id={}&phone={}'.format(self.permit_id, self.phone_number)
    #
    #     # send SMS to User
    #     self.send_sms(self.phone_number, link)
    #
    #     self.response.write('Thank you for your request. You should receive a text message with a link to the permit application. <br>')
    #     self.response.write(link)
    #
    #     #self.render('landing_page_form.html', **self.arg_dict)
    #
    # def send_sms(self, phone_number, link):
    #     # from twilio
    #     account_sid = "ACd686b67138bbee502e1d705fb3bcd19f"
    #     auth_token  = "f4ba6887175a913e6631af950e520299"
    #     twilio_phone_number = "+18324301720"
    #
    #     client = Client(account_sid, auth_token)
    #
    #     client.messages.create(
    #         to=phone_number,
    #         from_=twilio_phone_number.__str__(),
    #         body="Welcome to Aerwaze! Tap the link to apply for the permit. "+link,
    #         )