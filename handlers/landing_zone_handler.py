from handlers.enhanced_handler import EnhancedHandler
from databases.landing_zone import LandingZone
from databases.user import User
from my_email.my_email import LandingZoneEmailHandler
from google.appengine.ext import ndb
import urllib
import datetime
import json


class LandingZoneHandler(EnhancedHandler):

    def get(self):
        if not self.confirm_user_logged_in():
            self.redirect('/login')
            return
        self.add_page_name('landing_zone')
        self.arg_dict['lz'] = dict()
        self.arg_dict['lz']['start_time'] = LandingZoneInterface.make_now_date_dict()
        self.arg_dict['lz']['duration'] = 60
        self.arg_dict['lz']['radius'] = 1
        self.arg_dict['lz']['warning_text'] = 'A helicopter is landing in your area.  Please land your drone immediately.'
        #self.write(self.arg_dict['lz'])
        self.render('landing_zone_form.html', **self.arg_dict)

    def post(self):
        if not self.confirm_user_logged_in():
            self.redirect('/login')
            return
        if self.request.get('save_landing_zone'):
            self.add_page_name('landing_zone')
            lz_dict = LandingZoneInterface.read_inputs(self)
            if lz_dict['send_sms'] == 'true':
                LandingZoneEmailHandler().send_alert(lz_dict['warning_text'])
            this_user = User().by_user_name(self.user_name)
            lz = LandingZone()
            lz_key = lz.save_landing_zone(this_user.key,
                                          lz_dict['warning_text'],
                                          lz_dict['lat'],
                                          lz_dict['lng'],
                                          lz_dict['formatted_start_time'],
                                          lz_dict['formatted_end_time'],
                                          lz_dict['radius'])
            url_safe_key = lz_key.urlsafe()
            self.redirect('/landing_zone_edit/' + url_safe_key)


class LandingZoneEditHandler(EnhancedHandler):

    def get(self, resource):
        self.add_page_name('landing_zone')
        url_safe_key = urllib.unquote(resource)
        lz_key = ndb.Key(urlsafe=url_safe_key)
        lz = LandingZone.get_by_key(lz_key)
        self.arg_dict['lz'] = LandingZoneInterface.make_landing_zone_dictionary(lz)
        #self.write(self.arg_dict['lz'])
        self.render('landing_zone_form.html', **self.arg_dict)

    def post(self, resource):
        if not self.confirm_user_logged_in():
                self.redirect('/login')
                return
        url_safe_key = urllib.unquote(resource)
        lz_key = ndb.Key(urlsafe=url_safe_key)
        lz = LandingZone.get_by_key(lz_key)
        self.arg_dict['lz'] = LandingZoneInterface.make_landing_zone_dictionary(lz)
        if self.request.get('save_landing_zone'):
            self.add_page_name('landing_zone')
            lz_dict = LandingZoneInterface.read_inputs(self)
            this_user = User().by_user_name(self.user_name)
            lz_key = lz.update_landing_zone(this_user.key,
                                          lz_dict['warning_text'],
                                          lz_dict['lat'],
                                          lz_dict['lng'],
                                          lz_dict['formatted_start_time'],
                                          lz_dict['formatted_end_time'],
                                          lz_dict['radius'])
            url_safe_key = lz_key.urlsafe()
            self.redirect('/landing_zone_edit/' + url_safe_key)


class WithinLandingZoneHandler(EnhancedHandler):

    def get(self):
        lat = self.request.get('lat')
        lng = self.request.get('lng')
        if lat and lng:
            lat = float(lat)
            lng = float(lng)
            active_zones = LandingZone.point_within_landing_zone(lat, lng)
            active_zones_json = WithinLandingZoneHandler.make_landing_zone_response(active_zones)
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(active_zones_json)
        else:
            self.render('location_query_form.html')

    def post(self):
        lat = self.request.get('lat')
        lng = self.request.get('long')
        self.write(lat+lng)
        url = "/within_landing_zone?lat=" + lat + '&lng=' + lng
        self.redirect(url)

    @staticmethod
    def make_landing_zone_response(active_zones):
        active_zone_dict = dict()
        for zone in active_zones:
            active_zone_dict[zone.key.id()] = dict()
            active_zone_dict[zone.key.id()]['lat'] = zone.latitude
            active_zone_dict[zone.key.id()]['lng'] = zone.longitude
            active_zone_dict[zone.key.id()]['start_time'] = zone.start_time
            active_zone_dict[zone.key.id()]['duration'] = zone.duration
            active_zone_dict[zone.key.id()]['radius'] = zone.radius
            active_zone_dict[zone.key.id()]['warning_text'] = zone.warning_text
        active_zone_json = json.dumps(active_zone_dict)
        return active_zone_json


class LandingZoneInterface(EnhancedHandler):

    @staticmethod
    def make_landing_zone_dictionary(lz):
        lz_dict = dict()
        lz_dict['start_time'] = LandingZone.split_date_string(lz.start_time)
        lz_dict['duration'] = lz.duration
        lz_dict['radius'] = lz.radius
        lz_dict['warning_text'] = lz.warning_text
        lz_dict['lat'] = lz.latitude
        lz_dict['lng'] = lz.longitude
        return lz_dict

    @staticmethod
    def read_inputs(document):
        lz_dict = dict()
        lz_dict['start_time'] = document.request.get('start_time')
        lz_dict['duration'] = int(document.request.get('duration'))
        lz_dict['radius'] = int(document.request.get('radius'))
        lz_dict['warning_text'] = document.request.get('warning_text')
        lz_dict['send_sms'] = document.request.get('sms_checkbox')
        lz_dict['lat'] = float(document.request.get('lat'))
        lz_dict['lng'] = float(document.request.get('lng'))
        lz_dict['formatted_start_time'] = document.request.get('start_time')
        lz_dict['formatted_end_time'] = int(document.request.get('duration'))

        return lz_dict

    @staticmethod
    def make_now_date_dict():
        date_time = datetime.datetime.now()
        date_dict = dict()
        date_dict['month'] = date_time.month
        date_dict['day'] = date_time.day
        date_dict['year'] = date_time.year
        date_dict['hour'] = date_time.hour
        date_dict['minute'] = date_time.minute
        return date_dict