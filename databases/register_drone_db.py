from google.appengine.ext import ndb
import string
import random


class RegisterDrone(ndb.Model):
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    serial_number = ndb.StringProperty(required=True)
    manufacturer = ndb.StringProperty()
    model = ndb.StringProperty()
    year = ndb.StringProperty()
    insurer = ndb.StringProperty()
    policy_number = ndb.StringProperty()
    property_tag = ndb.StringProperty()
    drone_status = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def get_by_serial_number(serial_number):
        return RegisterDrone.query(RegisterDrone.serial_number == serial_number)

    @staticmethod
    def get_by_property_tag(property_tag):
        drone = RegisterDrone.query(RegisterDrone.property_tag == property_tag)
        for d in drone:
            return d

    @staticmethod
    def get_by_key(key):
        return RegisterDrone().get_by_id(key.id())

    @staticmethod
    def register_drone(first_name,
                       last_name,
                       email,
                       serial_number,
                       manufacturer,
                       model,
                       year,
                       insurer,
                       policy_number):
        property_tag = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        drone = RegisterDrone(first_name=first_name,
                              last_name=last_name,
                              email=email,
                              serial_number=serial_number,
                              manufacturer=manufacturer,
                              model=model,
                              year=year,
                              insurer=insurer,
                              policy_number=policy_number,
                              property_tag=property_tag,
                              drone_status='OK')
        drone_key = drone.put()
        return drone_key

    def update_drone(self,
                     first_name,
                     last_name,
                     email,
                     serial_number,
                     manufacturer,
                     model,
                     year,
                     insurer,
                     policy_number):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.serial_number = serial_number
        self.manufacturer = manufacturer
        self.model = model
        self.year = year
        self.insurer = insurer
        self.policy_number = policy_number
        key = self.put()
        return key

    @staticmethod
    def convert_to_dict_by_key(key):
        drone = RegisterDrone.get_by_key(key)
        drone_dict = {'first_name': drone.first_name,
                      'last_name': drone.last_name,
                      'email': drone.email,
                      'serial_number': drone.serial_number,
                      'manufacturer': drone.manufacturer,
                      'model': drone.model,
                      'year': drone.year,
                      'insurer': drone.insurer,
                      'policy_number': drone.policy_number,
                      'property_tag': drone.property_tag,
                      'drone_status': drone.drone_status,
                      'created': drone.created}
        return drone_dict