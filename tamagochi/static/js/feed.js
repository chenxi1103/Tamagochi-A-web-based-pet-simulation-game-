function getCSRFToken(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function(){
    $(".addbtn").click(function(e) {
        var item_id = $(this).val();

        $.post("feed", {"item_id":item_id}).done(function (data) {
            if(data.message != "") {
                alert(data.message);
            }
            location.reload();
        })
    });
});
