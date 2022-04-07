function inflateRepo(repo_json, label, template_id, container_id) {
    const template_copy = $(template_id).clone();
    $(template_copy).find(".repo-label").html(label);
    $(template_copy).find(".repo-location").html(repo_json.location);
    $(template_copy).find(".repo-latest-backup").html(repo_json.latest_backup);
    $(template_copy).find(".repo-size").html(repo_json.size);
    $(template_copy).find(".repo-recent-errors").html(repo_json.recent_errors);
    $(template_copy).find(".repo-size-graph").prop("id", `repo-${label}-size-graph`);

    let bg_class = "bg-primary";
    if (repo_json.error) {
        bg_class = "bg-danger";
    } else if (repo_json.warning) {
        bg_class = "bg-warning";
    }
    $(template_copy).addClass(bg_class);

    $(container_id).append(template_copy);
}


window.addEventListener("DOMContentLoaded", function () {
    // todo: inflate each repo and colour background accordingly
    const template = $('#repo-template').html();
    const container = $('#repo-container');

    $.getJSON(`/repo_list.json`, function (repo_list) {
        repo_list.labels.forEach(function (repo_label) {
            $.getJSON(`/repo/${repo_label}.json`, function (repo_json) {
                inflateRepo(repo_json, repo_label, template, container);
            })
        });
    })


    $.getJSON("repo_daily.json", function (json) {
        draw_time_graph("daily_backup_size", json.repos, json.dates, json.units);
    });
    $.getJSON("repo_monthly.json", function (json) {
        draw_time_graph("monthly_backup_size", json.repos, json.dates, json.units);
    });
}, false);
