function colourRepo(repo_json, label, container_id) {
    const repoLabel = `#repo-${label}`

    $(container_id).find(repoLabel).removeClass("bg-primary");

    let bg_class = "bg-primary";
    if (repo_json.error) {
        bg_class = "bg-danger";
    } else if (repo_json.warning) {
        bg_class = "bg-warning";
    }
    $(container_id).find(repoLabel).addClass(bg_class);
}

function stringRequests() {
    $('[data-json-string-request]').each(function (index, element) {
        $.getJSON($(this).attr("data-json-string-request"), function (data) {
            $(element).html(data['data']);
        })
    });
}

function colourRepos() {
    const container = $('#repo-container');
    $.getJSON(`/repo-list.json`, function (repo_list) {
        repo_list.labels.forEach(function (repo_label) {
            $.getJSON(`/repo/${repo_label}.json`, function (repo_json) {
                colourRepo(repo_json, repo_label, container);
            })
        });
    })
}

function createGraphs() {
    $.getJSON(`/repo-list.json`, function (repo_list) {
        repo_list.labels.forEach(function (repo_label) {
            $.getJSON(`/repo/${repo_label}/monthly-size.json`, function (repo_size_json) {
                draw_time_series_graph(`repo-${repo_label}-size-graph`, repo_size_json.repo,
                    repo_size_json.dates, repo_size_json.units);
            })
        });
    })
}

window.addEventListener("DOMContentLoaded", function () {
    setTimeout(createGraphs, 0);
    setTimeout(colourRepos, 0);
    setTimeout(stringRequests, 0);
}, false);
