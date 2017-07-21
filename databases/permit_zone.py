from google.appengine.ext import ndb

class PermitZone(ndb.Model):
    id = ndb.StringProperty() #"1001"
    name = ndb.StringProperty() #"Holbrook-Palmer Park"
    city = ndb.StringProperty() #"Atherton"
    location = ndb.GeoPtProperty()
    #type = ndb.

    @staticmethod
    def get_by_id(id):
        return PermitZone.query(PermitZone.id == id)

    @staticmethod
    def get_by_city(city):
        return PermitZone.query(PermitZone.city == city)

