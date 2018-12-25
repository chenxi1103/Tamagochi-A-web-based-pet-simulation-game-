function populate_status(){
  $.get("get_changes")
  .done(function(data){
    var list=$("#status");
    list.html('');
      Tamagochi = data["pet_self"];
      var new_status=data["html4"];
      list.prepend(new_status);
  })
}

function populate_age(){
  $.get("get_changes")
  .done(function(data){
    var age = $("#age");
    age.html('');
      Tamagochi = data["pet_self"];
      var new_age = data["html5"];
      age.prepend(new_age);
  })
}


$(document).ready(function(){
    populate_status();
    populate_age();
    window.setInterval(populate_status, 5000);
    window.setInterval(populate_age,60000);
    // CSRF set-up copied from Django docs
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
});
