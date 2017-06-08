/**
 * Created by cory1 on 10/14/2014.
 */
var map;
var myMarkers = [];
var currentPolyLines = [];
var polygonClosed = false;

function add_location_map() {
    var var_location = new google.maps.LatLng(40,-94);
    var markers = [];
    var var_mapoptions = {
      center: var_location,
      zoom: 4
    };

    map = new google.maps.Map(document.getElementById("map-container"),
        var_mapoptions);


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
        for (var i = 0, marker; marker = markers[i]; i++) {
            marker.setMap(null);
        }

        // For each place, get the icon, place name, and location.
        markers = [];
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

    //listen for clicks on the map and add markers and polyLines
    google.maps.event.addListener(map, 'click', function (event) {
        placeMarker(event.latLng);
    });
}



//handle adding and removing markers for the myMarkers array
//adds new marker to map and appends the markers array
function addMarker(location) {
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        draggable: true
    });
    myMarkers.push(marker);

    google.maps.event.addListener(marker, 'dragend', function () {
        markerDragEvent();
    });
}

//removes last marker from the markers array
function removeLastMarker() {
    myMarkers.pop();
}

//clear all markers from the markers array
function clearMarkers() {
    myMarkers = [];
}



//handle adding and removing polyLines from the currentPolyLines array
//adds a polyline to the map and appends the currentPolyLine array
function addPolyLine(markerOne, markerTwo) {
    var markerLocations = [];
    var pointOne = new google.maps.LatLng(markerOne.position.lat(), markerOne.position.lng());
    markerLocations.push(pointOne);
    var pointTwo = new google.maps.LatLng(markerTwo.position.lat(), markerTwo.position.lng());
    markerLocations.push(pointTwo);
    var currentPoly = new google.maps.Polyline({
        path: markerLocations,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    currentPolyLines.push(currentPoly);
}

//removes last polyl=Line from the currentPolyLine array
function removeLastPolyLine() {
    currentPolyLines.pop();
}

//clears all the polyLines from the currentPolyLine array
function clearPolyLines() {
    currentPolyLines = [];
}

//clears polyLines and the sets a new one for each marker in markers array
function resetPolyLines() {
    clearPolyLines();
    for (var i = 0; i < myMarkers.length-1; i++) {
        addPolyLine(myMarkers[i], myMarkers[i+1]);
    }
}



//handle placing and removing the markers and polyLines on the map
//places all markers and polyLines on the map
function placeAllMarkersOnMap(map) {
    placeMarkerBubblesOnMap(map);
    for (var i = 0; i < currentPolyLines.length; i++) {
        currentPolyLines[i].setMap(map);
    }
}

//places the markers bubbles on the map
function placeMarkerBubblesOnMap(map) {
    for (var i = 0; i < myMarkers.length; i++) {
        myMarkers[i].setMap(map);
    }
}

//removes the marker bubble from map
function removeMarkerBubblesFromMap() {
    placeMarkerBubblesOnMap(null);
}

//clears all markers from the map
function removeAllMarkersFromMap() {
    placeAllMarkersOnMap(null);
}

//clears all markers and polylines from variables and the map
function resetAllVariables() {
    removeAllMarkersFromMap();
    clearMarkers();
    clearPolyLines();
    polygonClosed = false;
}

//removes the last marker and polyline placed
function removeLastVariable() {
    removeAllMarkersFromMap();
    removeLastMarker();
    removeLastPolyLine();
    placeAllMarkersOnMap(map);
    polygonClosed = false;
}

//places the newest marker and polyline to the map
function placeMarker(location) {
    addMarker(location);
    myMarkers[myMarkers.length - 1].setMap(map);
    if (myMarkers.length > 1) {
        addPolyLine(myMarkers[myMarkers.length - 2], myMarkers[myMarkers.length - 1]);
        placeLastPolyLine()
    }
}

//sets the newest polyline to the map
function placeLastPolyLine() {
    currentPolyLines[currentPolyLines.length - 1].setMap(map);
}

//resets the map after a marker drag event
function markerDragEvent() {
    removeAllMarkersFromMap();
    resetPolyLines();
    placeAllMarkersOnMap(map);
}

//closes the polygon
function closePolygon() {
    if (polygonClosed == false && myMarkers.length > 2) {
        myMarkers.push(myMarkers[0]);
        addPolyLine(myMarkers[myMarkers.length - 2], myMarkers[myMarkers.length - 1]);
        polygonClosed = true;
        placeLastPolyLine();
    }
}

