/**
 * Created by cory1 on 10/17/2014.
 */

var map;
var myMarkers = [];
var markers = [];

function initialize_add_lz_map() {




    //if has marker center the marker on the screen and zoom
    if (lat != undefined && lng != undefined) {
        var myLatlng = new google.maps.LatLng(lat,lng);
        map = new google.maps.Map(document.getElementById('map-container'), {
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            zoom: 15,
            center: myLatlng
        });

        map.fitBounds(defaultBounds);
        var myMarker = new google.maps.Marker({
            position: myLatlng,
            map: map,
            draggable: true
        });
        myMarkers.push(myMarker);
        google.maps.event.addListener(myMarker, 'dragend', function () {
        markerDragEvent();
        });
        myMarkers[0].setMap(map);

    //if does not have marker render default map of the United States
    } else {
        map = new google.maps.Map(document.getElementById('map-container'), {
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });
        var defaultBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(50, -120),
        new google.maps.LatLng(30, -75));
        map.fitBounds(defaultBounds);
    }


    // Create the search box and link it to the UI element.
    var input = /** @type {HTMLInputElement} */(
        document.getElementById('pac-input'));
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    var searchBox = new google.maps.places.SearchBox(
        /** @type {HTMLInputElement} */(input));

    // [START region_getplaces]
    // Listen for the event fired when the user selects an item from the
    // pick list. Retrieve the matching places for that item.
    google.maps.event.addListener(searchBox, 'places_changed', function () {
        var places = searchBox.getPlaces();
        if (places.length == 0) {
            return;
        }
        //for (var i = 0, marker; marker = markers[i]; i++) {
        //  marker.setMap(null);
        //}

        // For each place, get the icon, place name, and location.
        //markers = [];
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
            /*var marker = new google.maps.Marker({
                map: map,
                icon: image,
                title: place.name,
                position: place.geometry.location
            });

            markers.push(marker);*/

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
        placeOneMarker(event.latLng);
    });

}

//place marker on the map
function placeOneMarker(location) {
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        draggable: true
    });
    placeMarkerBubblesOnMap(null);
    myMarkers = [];
    myMarkers.push(marker);
    google.maps.event.addListener(marker, 'dragend', function () {
        markerDragEvent();
    });
    myMarkers[0].setMap(map);
}

//create a child node using the id of the element
function createChildById(name, elementID, form) {
    var thisChild = document.createElement("input");
    thisChild.setAttribute("name", name);
    thisChild.setAttribute("value", document.getElementById(elementID).value);
    thisChild.setAttribute("type", "hidden");
    form.appendChild(thisChild);
    return form;
}

//create a child node by giving a name and a value
function createChildByValue(name, value, form) {
    var thisChild = document.createElement("input");
    thisChild.setAttribute("name", name);
    thisChild.setAttribute("value", value);
    thisChild.setAttribute("type", "hidden");
    form.appendChild(thisChild);
    return form;
}

//make sure there is a marker placed and create the form that gets returned to the server
function saveLandingZone() {
    if (myMarkers.length === 0) {
        window.alert("Please select a location!");
    } else {
        var form = document.createElement("FORM");
		document.body.appendChild(form);
        form.setAttribute('method', 'post');
        form.setAttribute('action', window.location.pathname);
        date_time = new Date($('#start_time_id').data().date).toISOString();
        form = createChildByValue('start_time', date_time, form);
        form = createChildById('duration', 'duration_id', form);
        form = createChildById('radius', 'radius_id', form);
        form = createChildById('warning_text', 'warning_area_id', form);
        form = createChildByValue('sms_checkbox', document.getElementById('sms_id').checked, form);
        form = createChildByValue('lat', myMarkers[0].position.lat(), form);
        form = createChildByValue('lng', myMarkers[0].position.lng(), form);
        form = createChildByValue("save_landing_zone", "true", form);
        //console.log(date_time);
        //console.log(form);
        form.submit();
    }
}