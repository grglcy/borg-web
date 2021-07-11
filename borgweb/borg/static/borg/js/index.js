window.addEventListener("DOMContentLoaded", function () {
    $.getJSON( "repo_daily.json", function( json ) {
        draw_time_graph("daily_backup_size", json.repos, json.dates, json.units);
     });
    $.getJSON( "repo_monthly.json", function( json ) {
        draw_time_graph("monthly_backup_size", json.repos, json.dates, json.units);
     });
}, false);
