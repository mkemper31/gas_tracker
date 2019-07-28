$(document).ready(function() {
    let ctx = document.getElementById('myChart').getContext('2d');
    data_dict = data_dict.replace(/'/g, '"');
    parsed_data = JSON.parse(data_dict);
    console.log(parsed_data['dates'])
    let chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: parsed_data['dates'],
            datasets: [{
                label: 'Miles Per Gallon',
                borderColor: 'blue',
                data: parsed_data['miles_per_gallon'],
                trendlineLinear: {
                    style: "rgb(43 ,66 ,255, 0.5)",
                    lineStyle: "dotted",
                    width: 2
                }
            }]
        },

        // Configuration options go here
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: false
                    }
                }]
            },
        }
    });
})