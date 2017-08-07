from google.appengine.ext import ndb
from databases.user import User

class Permit(ndb.Model):
    owner = ndb.StructuredProperty(User)
    name = ndb.StringProperty()
    geo_location = ndb.GeoPtProperty()
    city = ndb.StringProperty()
    type = ndb.StringProperty(choices=['Park', 'School', 'Airport'])
    creation_date = ndb.DateTimeProperty(auto_now_add=True)
    start_date = ndb.DateTimeProperty()
    end_date = ndb.DateTimeProperty()
    cost = ndb.StringProperty()
    #form = ndb.StructuredProperty(PermitForm)

    @staticmethod
    def get_owner(owner):
        permit = Permit.query(Permit.owner == owner)
        if permit.count() > 0:
            for p in permit:
                return p
        else:
            return False

    @staticmethod
    def add_new_permit(owner, name, type): # geo_location
        permit = Permit(owner=owner,
                        #geolocation=geo_location,
                        name=name,
                        type=type,
                        )
        p = permit.put()
        return p

class PermitForm(ndb.Model):
    user = ndb.StructuredProperty(User)
    permit = ndb.StructuredProperty(Permit)
    uav_model = ndb.StringProperty()
    uav_make = ndb.StringProperty()
    description = ndb.StringProperty()
    flight_date = ndb.DateTimeProperty()
    creation_date = ndb.DateTimeProperty(auto_now_add=True)
    status = ndb.StringProperty(default='pending')
    city = ndb.StringProperty()
    type = ndb.StringProperty(choices=['Recreational', 'Commercial', 'Official'])


    @staticmethod
    def create_permit_form(user_key, permit, uav_model, uav_make, description, flight_date):
        permit_form = PermitForm(parent=ndb.Key(permit.kind(), permit.id()),
                              user = user_key,
                              uav_model=uav_model,
                              uav_make=uav_make,
                              description=description,
                              flight_date=flight_date)
        p = permit_form.put()
        return p

    # @staticmethod
    # def get_by_key(permit_ndb_key):
    #     pk = PermitForm.query(PermitForm.key == permit_ndb_key)
    #     if pk.count() > 0:
    #         for p in pk:
    #             return p
    #     else:
    #         return False