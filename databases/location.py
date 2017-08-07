from google.appengine.ext import ndb
from databases.user import User

class FlyingLocation(ndb.Model):
    #geolocation = ndb.GeoPtProperty()
    lat = ndb.StringProperty()
    lon = ndb.StringProperty()
    user = ndb.StructuredProperty(User)
    time = ndb.StringProperty()
    date = ndb.StringProperty()

    # @staticmethod
    # def create_new(user, lat, lon, time):
    #     latlon = '%s, %s' %(lat, lon)
    #     #print latlon, time
    #     geolocation = ndb.GeoPt(latlon)
    #     p = FlyingLocation(user=user,
    #                        geolocation=geolocation,
    #                        time=time)
    #
    #     pn = p.put()
    #     return pn