var chart = new Chart("myChart", {
    type: "line",
    data: {
        datasets: [
        {
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(0,0,255,1.0)",
            borderColor: "rgba(0,0,255,0.1)",
            data: []
        },
        {
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(255,0,0,1.0)",
            borderColor: "rgba(255,0,0,0.1)",
            data: []
        },
    ]
    },
    options: {
        legend: { display: false },
        scales: {
            xAxes: [{
                type: 'time',
                scaleLabel: {
                    display: false,
                    labelString: 'Hours' // we can put other labels as well but just for example
                }
            }],
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Voltage/Steps'
                },
                // ticks: { min: 6, max: 16 }
            }]
        }
    }
});
