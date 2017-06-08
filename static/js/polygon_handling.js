/**
 * Created by cory1 on 10/17/2014.
 */
//
function saveLocation() {
    if (confirmClosedPolygon() == true) {
        var form = document.createElement("form");
        form.setAttribute('method', 'post');
        form.setAttribute('action', window.location.pathname);

        var location = document.createElement("input");
        location.setAttribute("name", "sight_name_location_name");
        location.setAttribute("value", document.getElementById("sight_name_location_id").value);
        form.appendChild(location);

        var points = makePointsForm();
        form.appendChild(points);
        document.body.appendChild(form);
        form.submit();
    }
}

function makePointsForm() {
    var pointsString = '';
    for (var i = 0; i < myMarkers.length; i++) {
        var lat = myMarkers[i].position.lat();
        var lng = myMarkers[i].position.lng();
        pointsString += lat.toString() + ',' + lng.toString() + '|';
    }
    pointsString = pointsString.slice(0, pointsString.length - 1);
    var points = document.createElement("input");
    points.setAttribute("name", "points_string_name");
    points.setAttribute("value", pointsString);
    points.setAttribute("type", "hidden");
    return points;
}

function convert_points_to_markers() {
    for (var i = 0; i < points.length-1; i++) {
        var location = { lat: points[i][0], lng: points[i][1] }
        placeMarker(location);
    }
    closePolygon();
}

function createChildById(name, elementID, form) {
    var thisChild = document.createElement("input");
    thisChild.setAttribute("name", name);
    thisChild.setAttribute("value", document.getElementById(elementID).value);
    thisChild.setAttribute("type", "hidden");
    form.appendChild(thisChild);
    return form;
}

function createChildByValue(name, value, form) {
    var thisChild = document.createElement("input");
    thisChild.setAttribute("name", name);
    thisChild.setAttribute("value", value);
    thisChild.setAttribute("type", "hidden");
    form.appendChild(thisChild);
    return form;
}

function editLocation() {
    if (confirmClosedPolygon() == true) {
        var form = document.createElement("FORM");
        form.setAttribute('method', 'post');
        form.setAttribute('action', window.location.pathname);

        var points = makePointsForm();
        form.appendChild(points);
        form = createChildById("descriptive_name", "sight_name_location_id", form);
        form = createChildById("active", "active_dropdown_id", form);
        form = createChildById("camera", "camera_dropdown_id", form);
        form = createChildById("camera_text", "camera_text_area_id", form);
        form = createChildById("video", "video_dropdown_id", form);
        form = createChildById("video_text", "video_text_area_id", form);
        form = createChildByValue("save_location", "true", form);
        form = createChildById("zip_code", "zip_code_id", form);
        console.log(form)
        document.body.appendChild(form);
        form.submit();
    }
}

function confirmClosedPolygon() {
    if (myMarkers.length < 3) {
        window.alert("A location requires at least 3 markers");
        return false;
    }
    if (closed == false) {
        closePolygon();
    }
    return true;
}

function deleteLocation() {
    var r = window.confirm("Are you sure you wish to delete this location?")
    if (r == true) {
        var form = document.createElement("form");
        form.setAttribute('method', 'post');
        form.setAttribute('action', window.location.pathname);
        form = createChildByValue("delete_location", "true", form);
        document.body.appendChild(form);
        form.submit();
    }
    else {
        return;
    }
}