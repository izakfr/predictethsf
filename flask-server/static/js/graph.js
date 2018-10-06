'use strict';

var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var config = {
    type: 'line',
    data: {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [{
            label: "dataset - Reviews",
            data: [
                3,
                18,
                79,
                182,
                322,
                391,
                413
            ],
            backgroundColor: window.chartColors.red,
            borderColor: window.chartColors.red,
            fill: false,
            borderDash: [5, 5],
            pointRadius: 5,
            pointHoverRadius: 10
        }, {
            label: "dataset - Bookmarks",
            data: [
                23,
                63,
                79,
                276,
                312,
                400,
                486
            ],
            backgroundColor: window.chartColors.blue,
            borderColor: window.chartColors.blue,
            fill: false,
            borderDash: [5, 5],
            pointRadius: [2, 4, 6, 18, 0, 12, 20]
        }, {
            label: "dataset - Views",
            data: [
                79,
                175,
                296,
                343,
                412,
                513,
                599
            ],
            backgroundColor: window.chartColors.green,
            borderColor: window.chartColors.green,
            fill: false,
            pointHoverRadius: 30
        }, {
            label: "dataset - Listings",
            data: [
                1,
                3,
                3,
                5,
                6,
                9,
                12
            ],
            backgroundColor: window.chartColors.yellow,
            borderColor: window.chartColors.yellow,
            fill: false,
            pointHitRadius: 5
        }]
    },
    options: {
        responsive: true,
        legend: {
            position: 'bottom'
        },
        hover: {
            mode: 'index'
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Month'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Value'
                }
            }]
        },
        title: {
            display: true,
            text: 'Account activity Visualization'
        }
    }
};

window.onload = function() {
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx, config);
};