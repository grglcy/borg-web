function inflateRepo(repo_json, label, template_id, container_id) {
    const repoLabel = `#repo-${label}`

    $(container_id).find(repoLabel).find(".repo-latest-backup").html(repo_json.latest_backup);
    $(container_id).find(repoLabel).find(".repo-size").html(repo_json.size);
    $(container_id).find(repoLabel).find(".repo-recent-errors").html(repo_json.recent_errors);

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
    const template = $('#repo-template').html();
    const container = $('#repo-container');

    $.getJSON(`/repo_list.json`, function (repo_list) {
        repo_list.labels.forEach(function (repo_label) {
            $.getJSON(`/repo/${repo_label}.json`, function (repo_json) {
                inflateRepo(repo_json, repo_label, template, container);
            })

            $.getJSON(`/repo/${repo_label}/size.json`, function (repo_size_json) {
                draw_time_series_graph(`repo-${repo_label}-size-graph`, repo_size_json.repo,
                    repo_size_json.dates, repo_size_json.units);
            })

        });
    })


    // $.getJSON("repo_daily.json", function (json) {
    //     draw_time_graph("daily_backup_size", json.repos, json.dates, json.units);
    // });
    // $.getJSON("repo_monthly.json", function (json) {
    //     draw_time_graph("monthly_backup_size", json.repos, json.dates, json.units);
    // });
}, false);
