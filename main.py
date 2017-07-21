#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

from handlers.landing_page_handler import LandingPageHandler
from handlers.signup_handler import SignUpHandler
from handlers.logout_handler import LogoutHandler
from handlers.login_handler import LoginHandler
from handlers.add_location_handler import AddLocationHandler
from handlers.edit_location_handler import EditLocationHandler
from handlers.edit_location_handler import JustTheMapHandler
from handlers.manage_locations_handler import ManageLocationsHandler
from search import location_search as ls
from handlers.landing_zone_handler import LandingZoneHandler
from handlers.landing_zone_handler import LandingZoneEditHandler
from handlers.landing_zone_handler import WithinLandingZoneHandler
import handlers.regulation_handler as regs
from handlers.permit_handler import PermitCreater
from handlers.permit_handler import PermitApplier
from handlers.permit_handler import PermitReviewer
from handlers.permit_handler import PermitApplication
from handlers.fly_handler import PreFlight

from register_drone.register_drone_handler import RegisterDroneHandler
from register_drone.register_drone_handler import LostDrone



app = webapp2.WSGIApplication([('/', LandingPageHandler),
                               ('/signup', SignUpHandler),
                               ('/logout', LogoutHandler),
                               ('/login', LoginHandler),
                               ('/add_location', AddLocationHandler),
                               ('/edit_location/([^/]+)?', EditLocationHandler),
                               ('/just_map', JustTheMapHandler),
                               ('/manage_locations', ManageLocationsHandler),
                               ('/radius', ls.LocationsWithinRadius),
                               ('/within_location', ls.LocationsThatContainPoint),
                               ('/radius_with_map', ls.LocationsNearbyUsingMap),
                               ('/within_location_with_map', ls.LocationsThatContainPointUsingMap),
                               ('/add_regulation', regs.AddRegulation),
                               ('/get_regulation_old', regs.GetRegulation),
                               ('/get_regulation', regs.GetRegulationWriter),
                               ('/write_regulation', regs.WriteRegulation),
                               ('/landing_zone', LandingZoneHandler),
                               ('/landing_zone_edit/([^/]+)?', LandingZoneEditHandler),
                               ('/within_landing_zone', WithinLandingZoneHandler),
                               ('/register_drone', RegisterDroneHandler),
                               ('/drone_status', LostDrone),
                               ('/locations_by_zip', ls.LocationsWithinZipCode),
                               ('/permit_create', PermitCreater),
                               ('/permit_apply', PermitApplier),
                               ('/permit_apply/[\w]', PermitApplication),
                               ('/permit_apply/atherton', PermitApplication),
                               ('/permit_review', PermitReviewer),
                               ('/preflight', PreFlight)

], debug=True)
