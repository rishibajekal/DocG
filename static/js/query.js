$(document).ready(readyFunc);

function readyFunc() {
    var sBtnSelector = $("#search-btn");
    sBtnSelector.click(function(event) {
        event.preventDefault();
        submitQuery();
    });
    showHelpTooltip();
}

function showHelpTooltip() {
    var searchBox = $("#search-box");

    searchBox.tooltip({
        'trigger':'focus',
        'placement': 'left',
        'title': 'Write a description of your symptoms here to get a diagnosis.'
    });

    searchBox.tooltip('show');

}

function submitQuery() {
    var searchQuery = $("#search-box").val();

    if (searchQuery !== "") {
        $.ajax('/search', {
            data: JSON.stringify({'query': searchQuery}),
            dataType: 'json',
            type: 'POST',
            success: function (response) {
                if (response.success) {
                    displayResults(response);
                }
                else {
                    displayEmptyResults();
                }
            },
            error: function () {
                displayError();
            }
        });
    }
    return false;
}

function displayEmptyResults() {
    clearResults();

    var html = "<h3>No illnesses match your symptoms. Please see a doctor for more information.</h3>";
    insertHtml(html);
}

function displayError() {
    clearResults();

    var html = "<h3>An error occurred while searching for your illness. Please try again.</h3>";
    insertHtml(html);
}

function displayResults(response) {
    clearResults();

    var doc_ids = response.data;
    var html = "<h3>Illnesses matching your symptoms:</h3><ul>";
    for (var i = 0; i < doc_ids.length; i++) {
        var did = doc_ids[i];
        html += "<li><h3>" + did + "</h3></li>";
    }
    html += "</ul>";

    insertHtml(html);
}

function insertHtml(html) {
    var resultDiv = $("#results");
    resultDiv.html(html);
}

function clearResults() {
    var resultDiv = $("#results");
    resultDiv.empty();
}