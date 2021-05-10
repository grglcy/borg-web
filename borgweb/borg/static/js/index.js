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
                            if (context.parsed.y !== null) {
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
                    display: true,
                    min: 0,
                    source: "ticks",
                    ticks: {
                        callback: function (value, index, values) {
                            if (value !== 0) {
                                return `${value} ${y_units}`
                            }
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

function getBaseLog(x, y) {
  return Math.log(y) / Math.log(x);
}