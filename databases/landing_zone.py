from google.appengine.ext import ndb
import math
import datetime


class LandingZone(ndb.Model):
    """This class creates a ndb object for describing a private location."""
    user_fk = ndb.KeyProperty(kind='User')
    warning_text = ndb.TextProperty()
    latitude = ndb.FloatProperty()
    longitude = ndb.FloatProperty()
    center = ndb.GeoPtProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    start_time = ndb.StringProperty()
    duration = ndb.IntegerProperty()
    end_time = ndb.DateTimeProperty()
    radius = ndb.IntegerProperty()

    @staticmethod
    def save_landing_zone(user_fk,
                          warning_text,
                          latitude,
                          longitude,
                          start_time,
                          duration,
                          radius):
        end_time = LandingZone.make_end_time(start_time, duration)
        landing_zone = LandingZone(user_fk=user_fk,
                                   warning_text=warning_text,
                                   latitude=latitude,
                                   longitude=longitude,
                                   center=ndb.GeoPt(latitude,longitude),
                                   start_time=start_time,
                                   duration=duration,
                                   end_time=end_time,
                                   radius=radius)
        landing_zone_key = landing_zone.put()
        return landing_zone_key

    @staticmethod
    def get_by_key(lz_key):
        return LandingZone().get_by_id(lz_key.id())

    @staticmethod
    def get_all_for_user(user):
        return LandingZone().query(LandingZone.user_fk == user.key)


    def update_landing_zone(self,
                            user_fk,
                            warning_text,
                            latitude,
                            longitude,
                            start_time,
                            duration,
                            radius):
        self.user_fk = user_fk
        self.warning_text = warning_text
        self.latitude = latitude
        self.longitude = longitude
        self.center = ndb.GeoPt(latitude,longitude)
        self.start_time = start_time
        self.duration = duration
        self.end_time = LandingZone.make_end_time(start_time, duration)
        self.radius = radius
        return self.put()

    @staticmethod
    def split_date_string(date_string):
        date_list = date_string.split('T')
        date_date = [int(x) for x in date_list[0].split('-')]
        date_hour = date_list[1].split(':')
        date_dict = dict()
        date_dict['month'] = date_date[1]
        date_dict['day'] = date_date[2]
        date_dict['year'] = date_date[0]
        date_dict['hour'] = int(date_hour[0])
        date_dict['minute'] = int(date_hour[1])
        return date_dict

    @staticmethod
    def make_end_time(start_time_string, duration):
        date_dict = LandingZone.split_date_string(start_time_string)
        start_date_time = datetime.datetime(date_dict['year'],
                                            date_dict['month'],
                                            date_dict['day'],
                                            date_dict['hour'],
                                            date_dict['minute'])
        end_date_time = start_date_time + datetime.timedelta(minutes=duration)
        return end_date_time

    @staticmethod
    def distance_between_points(lat1, lng1, lat2, lng2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)
        a = (math.sin(dlat/2.) * math.sin(dlat/2.)) + \
            (math.sin(dlng/2.) * math.sin(dlng/2.) * math.cos(lat1) * math.cos(lat2))
        c = 2. * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c
        return d

    @staticmethod
    def distance_between_points_in_miles(lat1, lng1, lat2, lng2):
        return .621371 * LandingZone.distance_between_points(lat1, lng1, lat2, lng2)

    @staticmethod
    def point_within_landing_zone(lat, lng):
        time_now = datetime.datetime.now()
        active_zones = LandingZone.query(LandingZone.end_time >= time_now)
        active_zones_within_radius = list()
        for zone in active_zones:
            if zone.radius >= LandingZone.distance_between_points_in_miles(lat, lng, zone.latitude, zone.longitude):
                active_zones_within_radius.append(zone)
        return active_zones_within_radius