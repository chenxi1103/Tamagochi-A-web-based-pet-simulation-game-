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
        var friend_id = $("#friend_id").attr("value");

        $.post("/tamagochi/feedFriend", 
            {
                "item_id":item_id, 
                "friend_id":friend_id, 
                "csrfmiddlewaretoken": getCSRFToken("csrftoken")
            }
        ).done(function(data) {
            if(data.message != "") {
                alert(data.message);
            }
            location.reload();
        })
    });
});