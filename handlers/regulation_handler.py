from handlers import enhanced_handler as eh
from databases import regulation as reg
from databases import regulation_writer as reg_writer
from google.appengine.api import urlfetch
import json


class AddRegulation(eh.EnhancedHandler):
    def get(self):
        self.render('add_regulation.html', **self.arg_dict)

    def post(self):
        city_name = self.request.get('cityNameInput').lower()
        zip_code = self.request.get('zipCodeInput').lower()
        regulation = self.request.get('regulationInput')
        new_regulation_key = reg.ZipCode().add_zip_code(zip_code, city_name, regulation)
        self.write(new_regulation_key)


class GetRegulation(eh.EnhancedHandler):
    def get(self):
        zip_code = self.request.get('zipCode').lower()
        city_name = self.request.get('city').lower()
        lat_lng = self.request.get('latLng').replace(" ","")
        data_type = self.request.get('format').lower()
        regulations = None
        self.add_page_name("regulation")
        if zip_code:
            regulations = reg.ZipCode.get_by_zip_code(zip_code)
        elif city_name:
            regulations = reg.ZipCode.get_by_city_name(city_name)
        elif lat_lng:
            url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="
            url += lat_lng
            url += "&key=AIzaSyBYZ4U65PtFBrIpAimLtporw8ehdvXBo6k"
            response = urlfetch.fetch(url)
            if response.status_code == 200:
                data = json.loads(response.content)
                zip_code = data['results'][0]['address_components'][-2]['long_name']
                regulations = reg.ZipCode.get_by_zip_code(zip_code)
        else:
            self.render('get_regulation.html', **self.arg_dict)
            return
        all_regulations = None
        if regulations and regulations.count() != 0:
            all_regulations = GetRegulation.make_regulations_list(regulations)
        if data_type == "json":
            self.response.headers["Content-Type"] = "application/json"
            json_regulations = json.dumps(all_regulations)
            self.response.out.write(json_regulations)
        else:
            if all_regulations:
                self.arg_dict["regulations"] = all_regulations
            self.render("show_regulations.html", **self.arg_dict)

    @staticmethod
    def make_regulations_list(regulations):
        all_regulations = list()
        for regulation in regulations:
            result = dict()
            result['city'] = regulation.city.title()
            result['regulation'] = regulation.regulation
            result['zip_code'] = regulation.zip_code
            all_regulations.append(result)
        return all_regulations


class WriteRegulation(eh.EnhancedHandler):
    def get(self):
        self.render("write_regulation.html", **self.arg_dict)

    def post(self):
        city_name = self.request.get('cityNameInput').lower()
        zip_codes = self.request.get('zipCodeInput').split()
        allow = self.request.get('allow_name')
        if allow == 'allow':
            allow = True
        else:
            allow = False
        license_requirement = self.request.get('license_name')
        if license_requirement == 'require':
            license_requirement = True
        elif license_requirement == 'not_require':
            license_requirement = False
        else:
            license_requirement = None
        license_type = self.request.get('license_type_name')
        if license_type not in ['generic', 'specific']:
            license_type = None
        insurance = self.request.get('insurance_name')
        if insurance == 'require':
            insurance = True
        elif insurance == 'not_require':
            insurance = False
        else:
            insurance = None
        everywhere = self.request.get('everywhere_name')
        if everywhere == 'everywhere':
            everywhere = True
        elif everywhere == 'zones':
            everywhere = False
        else:
            everywhere = None
        white_black = self.request.get('white_black_name')
        if white_black not in ['white', 'black']:
            white_black = None
        reg_keys = list()
        for zip_code in zip_codes:
            key = reg_writer.RegulationWriter().add_new_regulation(zip_code,
                                                                   city_name,
                                                                   allow,
                                                                   license_requirement,
                                                                   license_type,
                                                                   insurance,
                                                                   everywhere,
                                                                   white_black)
            reg_keys.append(key)
        self.write(reg_keys)


class GetRegulationWriter(eh.EnhancedHandler):
    def get(self):
        zip_code = self.request.get('zipCode')
        lat_lng = self.request.get('latLng').replace(" ","")
        format_type = self.request.get('format').lower()
        regulations = None
        regulation_list = list()
        if len(lat_lng) == 0 and len(zip_code) == 0:
            self.render('get_regulation.html', **self.arg_dict)
        else:
            if lat_lng:
                url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="
                url += lat_lng
                url += "&key=AIzaSyBYZ4U65PtFBrIpAimLtporw8ehdvXBo6k"
                response = urlfetch.fetch(url)
                if response.status_code == 200:
                    data = json.loads(response.content)
                    zip_code = data['results'][0]['address_components'][-2]['long_name']
            if zip_code:
                regulations = reg_writer.RegulationWriter.get_by_zip_code(zip_code)
            if regulations:
                for regulation in regulations:
                    regulation_list.append(regulation.convert_regulation_to_dictionary())
            if format_type == 'json':
                regulation_list = json.dumps(regulation_list)
                self.response.headers['Content-Type'] = 'application/json'
                self.response.out.write(regulation_list)
            else:
                self.write(regulation_list)