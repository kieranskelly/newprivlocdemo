from google.appengine.ext import ndb


class RegulationWriter(ndb.Model):
    zip_code = ndb.StringProperty()
    city_name = ndb.StringProperty()
    allow = ndb.BooleanProperty()
    license_requirement = ndb.BooleanProperty()
    license_type = ndb.StringProperty()
    insurance = ndb.BooleanProperty()
    everywhere = ndb.BooleanProperty()
    white_black = ndb.StringProperty()


    @staticmethod
    def add_new_regulation(zip_code,
                           city_name,
                           allow,
                           license_requirement,
                           license_type,
                           insurance,
                           everywhere,
                           white_black):
        new_regulation = RegulationWriter(zip_code=zip_code,
                                          city_name=city_name,
                                          allow=allow,
                                          license_requirement=license_requirement,
                                          license_type=license_type,
                                          insurance=insurance,
                                          everywhere=everywhere,
                                          white_black=white_black)
        return new_regulation.put()

    @staticmethod
    def get_by_zip_code(zip_code):
        return RegulationWriter.query(RegulationWriter.zip_code == zip_code)

    @staticmethod
    def get_by_city_name(city_name):
        return RegulationWriter.query(RegulationWriter.city_name == city_name)

    def convert_regulation_to_dictionary(self):
        regulation = dict()
        regulation['zip_code'] = self.zip_code
        regulation['city_name'] = self.city_name
        regulation['allow'] = self.allow
        regulation['license_requirement'] = self.license_requirement
        regulation['license_type'] = self.license_type
        regulation['insurance'] = self.insurance
        regulation['everywhere'] = self.everywhere
        regulation['white_black'] = self.white_black
        return regulation