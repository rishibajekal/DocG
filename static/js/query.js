$(document).ready(readyFunc);

function readyFunc() {
    var sBtnSelector = $("#search-btn");
    sBtnSelector.click(function(event) {
        event.preventDefault();
        submitQuery();
    });
}

function submitQuery() {
    var searchQuery = $("#search-box").val();

    if (searchQuery !== "") {
        $.ajax('/search', {
            data: JSON.stringify({'query': searchQuery}),
            dataType: 'json',
            type: 'POST',
            success: function (resp) { console.log(resp); },
            error: function () { console.log('error'); }
        });
    }
    return false;
}