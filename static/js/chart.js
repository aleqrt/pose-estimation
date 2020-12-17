var options = {
    series: [{
        data: [28, 29, 33, 36, 32, 32, 33]
    }],
    colors: ['#008FFB'],
    yaxis: {
        labels: {
            minWidth: 40
            }
        }
};

var chartLine = new ApexCharts(document.querySelector("#chart-line"), options);
chartLine.render();

var optionsLine2 = {
    series: [{
        data: [28, 29, 33, 36, 32, 32, 33]
    }],
    colors: ['#546E7A'],
    yaxis: {
        labels: {
            minWidth: 40
        }
    }
};

var chartLine2 = new ApexCharts(document.querySelector("#chart-line2"), optionsLine2);
chartLine2.render();

var optionsLine3 = {
    series: [{
        data: [28, 29, 33, 36, 32, 32, 33]
    }],
    colors: ['#546E7A'],
    yaxis: {
        labels: {
            minWidth: 40
        }
    }
};

var chartLine3 = new ApexCharts(document.querySelector("#chart-line3"), optionsLine3);
chartLine3.render();
