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


window.addEventListener("DOMContentLoaded", function () {
    // todo: inflate each repo and colour background accordingly
    const container = $('#repo-container');

    $('[data-json-string-request]').each(function (index, element) {
        $.getJSON($(this).attr("data-json-string-request"), function (data) {
            $(element).html(data['data']);
        })
    });

    $.getJSON(`/repo-list.json`, function (repo_list) {
        repo_list.labels.forEach(function (repo_label) {
            $.getJSON(`/repo/${repo_label}.json`, function (repo_json) {
                colourRepo(repo_json, repo_label, container);
            })

            $.getJSON(`/repo/${repo_label}/monthly-size.json`, function (repo_size_json) {
                draw_time_series_graph(`repo-${repo_label}-size-graph`, repo_size_json.repo,
                    repo_size_json.dates, repo_size_json.units);
            })

        });
    })

}, false);
