function draw_time_graph(chartID, repos, dateLabels, sizeUnits) {
    var datasets = []
    repos.forEach(function (repo) {
        datasets.push({
            label: repo.label,
            data: repo.size,
            fill: false,
            borderColor: 'rgb(75, 192, 192)'
        });
    })

    const data = {
        labels: dateLabels,
        datasets: datasets
    };

    const config = {
        type: 'line',
        data,
        options: {
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const yValue = context.parsed.y
                            if (yValue !== null) {
                                return `${yValue} ${sizeUnits}`
                            } else {
                                return ""
                            }
                        }
                    }
                }
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
                            return `${value} ${sizeUnits}`
                        }
                    }
                }
            }
        }
    }

    var myChart = new Chart(
        document.getElementById(chartID),
        config
    );
}
