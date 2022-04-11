function draw_time_series_graph(canvas, data) {
    let datasets = [{
        label: data.label,
        data: data.size,
        fill: false,
        borderColor: 'rgb(7, 59, 76)'
    }]

    const graphData = {
        labels: data.dates,
        datasets: datasets
    };

    const config = {
        type: 'line',
        data: graphData,
        options: {
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const yValue = context.parsed.y
                            if (yValue !== null) {
                                return `${yValue} ${data.units}`
                            } else {
                                return ""
                            }
                        }
                    }
                },
                legend: {
                    display: false
                },
            },
            scales: {
                y: {
                    min: 0,
                    title: {
                        display: true,
                        text: "Compressed Size",
                        font: {
                            size: 18
                        }
                    },
                    ticks: {
                        callback: function (value, index, values) {
                            return `${value} ${data.units}`
                        }
                    }
                }
            }
        }
    }

    const newGraph = new Chart(
        canvas,
        config
    );
}
