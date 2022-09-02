
$(document).ready(function() {
    $.ajax({
        method: "GET",
        url: "/version",
        success: function (data) {
            $(".version").html(data.version_string);
        }
    });
})