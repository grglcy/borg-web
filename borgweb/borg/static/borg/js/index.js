function inflateRepo(repo_json, label, template_id, container_id) {
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
    const template = $('#repo-template').html();
    const container = $('#repo-container');

    $('[data-json-string-request]').each(function (index, element) {
        $.getJSON($(this).attr("data-json-string-request"), function (data) {
            $(element).html(data['data']);
        })
    });
}, false);
