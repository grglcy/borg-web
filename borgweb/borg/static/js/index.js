
window.addEventListener("DOMContentLoaded", function() {
        const hour_json = JSON.parse(document.getElementById('hour_list').textContent);
        hour_json.forEach(function(repo) {
            console.log(repo.hours);
        })
        }, false);