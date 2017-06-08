from handlers.enhanced_handler import EnhancedHandler
from databases.register_drone_db import RegisterDrone


class RegisterDroneHandler(EnhancedHandler):

    def get(self):
        self.arg_dict['drone'] = {}
        self.add_page_name('register_drone')
        '''self.arg_dict['drone'] = {'first_name': 'Cory',
                                  'last_name': 'Stewart',
                                  'email': 'cory@gbar.com',
                                  'serial_number': '12345',
                                  'manufacturer': 'Blah',
                                  'model': 'xc650',
                                  'year': '1987',
                                  'insurer': 'Aetna',
                                  'policy_number': 10947576}'''

        self.render('drone_registry.html', **self.arg_dict)

    def post(self):
        self.add_page_name('register_drone')
        first_name = self.request.get('first_name_name')
        last_name = self.request.get('last_name_name')
        email = self.request.get('email_name')
        serial_number = self.request.get('serial_number_name')
        manufacturer = self.request.get('manufacturer_name')
        model = self.request.get('model_name')
        year = self.request.get('year_name')
        insurer = self.request.get('insurer_name')
        policy_number = self.request.get('policy_number_name')
        property_tag = self.request.get('property_tag_name')
        if property_tag:
            drone = RegisterDrone.get_by_property_tag(property_tag)
            drone_key = drone.key
            drone.update_drone(first_name,
                               last_name,
                               email,
                               serial_number,
                               manufacturer,
                               model,
                               year,
                               insurer,
                               policy_number)
        else:
            drone_key = RegisterDrone.register_drone(first_name,
                                                     last_name,
                                                     email,
                                                     serial_number,
                                                     manufacturer,
                                                     model,
                                                     year,
                                                     insurer,
                                                     policy_number)
        self.arg_dict['drone'] = RegisterDrone.convert_to_dict_by_key(drone_key)
        self.render('drone_registry.html', **self.arg_dict)


class LostDrone(EnhancedHandler):

    def get(self):
        self.add_page_name('found_drone')
        self.render('lost_drone_form.html', **self.arg_dict)

    def post(self):
        self.add_page_name('found_drone')
        property_tag = self.request.get('property_tag_name')
        drone = RegisterDrone.get_by_property_tag(property_tag)
        drone_status = self.request.get("drone_status_name")
        if drone:
            drone_key = drone.key
            if drone_status in ["Lost", "Stolen", "Found"]:
                drone.drone_status = drone_status
                drone.put()
                if drone_status in ["Lost", "Stolen"]:
                    self.arg_dict["drone_status"] = "lost_stolen"
                elif drone_status == "Found":
                    self.arg_dict["drone_status"] = "found"
                self.render("report_thank_you_form.html", **self.arg_dict)

            elif drone_status == "Check Status":
                self.arg_dict['drone'] = RegisterDrone.convert_to_dict_by_key(drone_key)
                self.render('drone_status_form.html', **self.arg_dict)
                #self.render('drone_registry.html', **self.arg_dict)

            elif drone_status == "Law Enforcement":
                self.arg_dict['drone'] = RegisterDrone.convert_to_dict_by_key(drone_key)
                self.render('drone_registry.html', **self.arg_dict)

        else:
            self.write('Property tag not found')