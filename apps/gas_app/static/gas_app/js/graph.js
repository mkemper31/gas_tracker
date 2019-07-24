$(document).ready(function() {
    var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: ['23 May 2019', '7 June 2019', '16 June 2019', '29 June 2019', '18 July 2019'],
            datasets: [{
                label: 'Miles Per Gallon',
                borderColor: 'rgb(255, 99, 132)',
                data: [18, 16, 20, 19, 15]
            }]
        },

        // Configuration options go here
        options: {}
    });
})