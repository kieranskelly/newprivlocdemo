from google.appengine.ext import ndb


class ZipCode(ndb.Model):
    zip_code = ndb.StringProperty()
    city = ndb.StringProperty()
    regulation = ndb.TextProperty()

    @staticmethod
    def add_zip_code(zip_code, city_name, regulation):
        new_zip = ZipCode(zip_code=zip_code,
                          city=city_name,
                          regulation=regulation)
        return new_zip.put()

    @staticmethod
    def get_by_zip_code(zip_code):
        return ZipCode.query(ZipCode.zip_code == zip_code)

    @staticmethod
    def get_by_city_name(city_name):
        return ZipCode.query(ZipCode.city == city_name)
