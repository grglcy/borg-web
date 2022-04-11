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
        });
    });
}

function graphRequests() {
    $('[data-json-graph-request]').each(function (index, element) {
        $.getJSON($(this).attr("data-json-graph-request"), function (data) {
            let newGraph = $('<canvas/>').width(400).height(200);
            draw_time_series_graph(newGraph, data)
            $(element).html(newGraph);
        });
    });
}

function colourRepos(repo_list) {
    const container = $('#repo-container');
    repo_list.labels.forEach(function (repo_label) {
        $.getJSON(`/repo/${repo_label}.json`, function (repo_json) {
            colourRepo(repo_json, repo_label, container);
        });
    });
}

window.addEventListener("DOMContentLoaded", function () {
    setTimeout(stringRequests, 0);
    setTimeout(graphRequests, 0);
    $.getJSON(`/repo-list.json`, function (repo_list) {
        setTimeout(colourRepos.bind(null, repo_list), 0);
    });
}, false);
