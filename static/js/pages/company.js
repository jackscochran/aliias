$(document).ready(function(){
    ticker = $('#tickerValue').val() 
    $.ajax({
        url: '/api/historical-prices',
        type: 'GET',
        data: {'ticker': ticker},
        async: true,
        dataType: 'JSON',
        success: function(data){

            var priceChart = new Chart('priceChart', {
                type: 'line',
                data: {
                    labels: data['results']['dates'],
                    datasets: [{
                        label: 'Historical Price Data',
                        data: data['results']['prices']
                    }]
                },
                options: {
                    legend: {
                        display: false
                    },
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'day'
                            }
                        },
                        xAxes: [{
                            ticks: {
                                display: false
                            },
                            gridLines: {
                                color: "rgba(0, 0, 0, 0)"
                            }
                        }],
                        yAxes: [{
                            gridLines: {
                                color: "rgba(0, 0, 0, 0)"
                            }
                        }]
                    }
                }
            });
        },
        error: function(){
            console.error('Company API called failed')
        }
    }); 

})