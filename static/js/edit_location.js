/**
 * Created by cory1 on 10/17/2014.
 */

var currentPolygons = [];
var map;
var myMarkers = [];
var currentPolyLines = [];
var polygonClosed = false;

function initialize_add_location_map() {

    var map_kind;
    if (typeof map_type === 'undefined') {
        map_kind = google.maps.MapTypeId.ROADMAP;
    }else if (map_type == 1) {
        map_kind = google.maps.MapTypeId.HYBRID;
    } else {
        map_kind = google.maps.MapTypeId.ROADMAP;
    }

    map = new google.maps.Map(document.getElementById('map-container'), {
            mapTypeId: map_kind,
            tilt: 0
        });

    var defaultBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(max_lat, min_long),
        new google.maps.LatLng(min_lat, max_long));
    map.fitBounds(defaultBounds);

    // Create the search box and link it to the UI element.
    var input = /** @type {HTMLInputElement} */(
        document.getElementById('pac-input'));
    var searchBox = new google.maps.places.SearchBox(
        /** @type {HTMLInputElement} */(input));
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);


    // [START region_getplaces]
    // Listen for the event fired when the user selects an item from the
    // pick list. Retrieve the matching places for that item.
    google.maps.event.addListener(searchBox, 'places_changed', function () {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
            return;
        }
        for (var i = 0, marker; marker = markers[i]; i++) {
            marker.setMap(null);
        }

        // For each place, get the icon, place name, and location.
        var markers = [];
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0, place; place = places[i]; i++) {
            var image = {
                url: place.icon,
                size: new google.maps.Size(71, 71),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(17, 34),
                scaledSize: new google.maps.Size(25, 25)
            };

            // Create a marker for each place.
            var marker = new google.maps.Marker({
                map: map,
                icon: image,
                title: place.name,
                position: place.geometry.location
            });

            markers.push(marker);

            bounds.extend(place.geometry.location);
        }

        map.fitBounds(bounds);
    });
    // [END region_getplaces]

    // Bias the SearchBox results towards places that are within the bounds of the
    // current map's viewport.
    google.maps.event.addListener(map, 'bounds_changed', function () {
        var bounds = map.getBounds();
        searchBox.setBounds(bounds);
    });

    google.maps.event.addListener(map, 'click', function (event) {
        placeMarker(event.latLng);
    });

}

//add to the existing map the points of the location
function edit_location_map() {
    initialize_add_location_map();
    convert_points_to_markers();
    if (typeof triangles != 'undefined') {
        createCurrentPolygons(triangles);
        placeCurrentPolygonsOnMap(map);
    }
}


function changeShowHideMarkersButton() {
    var btn =$('#show_hide_markers_id');
    if (btn.val() == 'Hide Markers') {
        btn.val('Show Markers');
        btn.text('Show Markers');
        removeMarkerBubblesFromMap();
    }
    else {
        btn.val('Hide Markers');
        btn.text('Hide Markers');
        placeMarkerBubblesOnMap(map);
    }
}

function changeShowHidePolygonsButton() {
    var btn = $('#show_hide_polygons_id');
    if (btn.val() == 'Hide Polygons') {
        btn.val('Show Polygons');
        btn.text('Show Polygons');
        hidePolygons();
    }
    else {
        btn.val('Hide Polygons');
        btn.text('Hide Polygons');
        placeCurrentPolygonsOnMap(map);
    }
}

function makePolygon(triangleArray) {
    var triangleCoords = [
        new google.maps.LatLng(triangleArray[0][0],
                               triangleArray[0][1]),
        new google.maps.LatLng(triangleArray[1][0],
                               triangleArray[1][1]),
        new google.maps.LatLng(triangleArray[2][0],
                               triangleArray[2][1])];
    var thisTriangle = new google.maps.Polygon({
        paths: triangleCoords,
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 3,
        fillColor: '#FF0000',
        fillOpacity: 0.35
    });
    currentPolygons.push(thisTriangle);
}

function createCurrentPolygons(triangles) {
    for (var i = 0; i < triangles.length; i++) {
        makePolygon(triangles[i]);
    }
}

function placeCurrentPolygonsOnMap(map) {
    for (var i = 0; i < currentPolygons.length; i++) {
        currentPolygons[i].setMap(map);
    }
}

function hidePolygons() {
    placeCurrentPolygonsOnMap(null);
}

function showPolygons() {
    placeCurrentPolygonsOnMap(map);
}