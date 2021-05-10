window.addEventListener("DOMContentLoaded", function () {
    const repoDict = JSON.parse(document.getElementById('hour_list').textContent);
    set_daily_graph(repoDict)
}, false);

function set_daily_graph(repoDict) {
    const labels = repoDict.date_labels;
    const y_units = repoDict.units

    var datasets = []
    repoDict.repos.forEach(function (repo) {
        datasets.push({
            label: repo.label,
            data: repo.daily_size,
            fill: false,
            tension: 0.1,
            borderColor: 'rgb(75, 192, 192)'
        });
    })

    const data = {
        labels: labels,
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
                            var label = context.dataset.label || '';
                            if (context.parsed.y !== null && y_units !== null) {
                                return `${context.parsed.y} ${y_units}`
                            } else {
                                return ""
                            }
                        }
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        display: true,
                        grid: false,
                        callback: function (value, index, values) {
                            return value + " " + y_units;
                        }
                    }
                }
            }
        }
    }

    var myChart = new Chart(
        document.getElementById('backup_csize_hourly'),
        config
    );
}