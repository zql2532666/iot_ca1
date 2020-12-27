function renderLDRChart(lightIntensity, labels){
    var ctx3 = document.getElementById("chart3").getContext('2d');
    var myChart3 = new Chart(ctx3, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Light Intensity',
                    data: lightIntensity,
                    borderColor: '#c56015',
                    borderWidth: 1,
                    fill: false
                }
            ],
            options: {
                scales: {
                    xAxes: [
                        {
                            type: 'time'
                        }
                    ]
                }
            }
        },
    });
}

function renderHumidityChart(humidity, labels){
    var ctx2 = document.getElementById("chart2").getContext('2d');

    
    var myChart2 = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'humidity (%)',
                    data: humidity,
                    borderColor: '#3b6431',
                    borderWidth: 1,
                    fill: false
                },
            ],
            options: {
                scales: {
                    xAxes: [
                        {
                            type: 'time'
                        }
                    ]
                }
            }
        },
    });
}

function renderTempChart(temp, labels) {
    var ctx = document.getElementById("chart").getContext('2d');
    
    
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'temperature (Degree Celcius)',
                    data: temp,
                    borderColor: '#3c0e7b',
                    borderWidth: 1,
                    fill: false
                }
            ],
            options: {
                scales: {
                    xAxes: [
                        {
                            type: 'time'
                        }
                    ]
                }
            }
        },
    });
}

var ctx = document.getElementById("chart").getContext('2d');
var tempChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [
            {
                label: 'temperature (Degree Celcius)',
                data: temp,
                borderColor: '#3c0e7b',
                borderWidth: 1,
                fill: false
            }
        ],
        options: {
            scales: {
                xAxes: [
                    {
                        type: 'time'
                    }
                ]
            }
        }
    },
});


var ctx2 = document.getElementById("chart2").getContext('2d');
var humidityChart = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'humidity (%)',
                    data: humidity,
                    borderColor: '#3b6431',
                    borderWidth: 1,
                    fill: false
                },
            ],
            options: {
                scales: {
                    xAxes: [
                        {
                            type: 'time'
                        }
                    ]
                }
            }
        },
});


var ctx3 = document.getElementById("chart3").getContext('2d');
var lightChart = new Chart(ctx3, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Light Intensity',
                    data: lightIntensity,
                    borderColor: '#c56015',
                    borderWidth: 1,
                    fill: false
                }
            ],
            options: {
                scales: {
                    xAxes: [
                        {
                            type: 'time'
                        }
                    ]
                }
            }
        },
});

function getHistoricalTempAndHumidity() {
        var dht11Data = {}
        dht11Data.temperatures = []
        dht11Data.humidity = []
        dht11Data.datetime = []
        $.ajax({
                url: "/api/dht11-data",
                async: false,
                success: function(results){
                            for(var i = 0; i < results.length; i++){
                                dht11Data.temperatures.push(results[i].temperature)
                                dht11Data.humidity.push(results[i].humidity)
                                dht11Data.datetime.push(results[i].datetime)
                            }
                        },
                
                type: 'GET'
            });

        return dht11Data
    };


function getHistoricalLightIntensity(){
        var LDRData = {}
        LDRData.lightIntensity = []
        LDRData.datetime = []
        $.ajax({
                url: "/api/ldr-data",
                async: false,
                success: function(results){
                            for(var i = 0; i < results.length; i++){
                                LDRData.lightIntensity.push(results[i].light_intensity)
                                LDRData.datetime.push(results[i].datetime)
                            }
                        },
                
                type: 'GET'
            });

        return LDRData
};


function updateGraphs(){
    var ldrdata = getHistoricalLightIntensity();
    var dht11Data = getHistoricalTempAndHumidity();
}


function updateTempChart(dataset){
    
}

function getCurrentDHT11Data(){
    $.ajax({
        url: "/api/latest-dht11-reading",
        success: function(results){
                    $('#temperature').html(results.temperature + " &deg;C");
                    $('#humidity').html(results.humidity + " %");
                },
        
        type: 'GET'
    });
};

function getCurrentLDRData(){
    $.ajax({
        url: "/api/latest-ldr-reading",
        success: function(results){
                    $('#light').html(results.light_intensity);
                },
        type: 'GET'
    });
};



$(document).ready(function() {
    getLEDStatus();
    updateGraphs();
    setInterval(getCurrentLDRData, 1000 * 5);
    setInterval(getCurrentDHT11Data, 1000 * 5);
});





