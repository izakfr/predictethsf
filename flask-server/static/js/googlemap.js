'use strict';

function myMap() {
    var location = {lat: 37.779161, lng: -122.414861};
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
        center: location
    });

    var marker = new google.maps.Marker({
        position: location,
        map: map,
        title: 'San Francisco, CA'
    });
}