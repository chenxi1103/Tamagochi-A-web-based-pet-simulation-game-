function get_message(){
  $.get('get_message')
  .done(function(data){
    var list=$("#invitation_list");
    list.html("");
    if (data.friends.length>0){
      for (i=0;i<data.friends.length;i++) {
        var friend=data.friends[i];
        var new_friend=$(friend.html7);
        list.append(new_friend);
      };
      $('#message_invitation').modal('show');
    }

  });
}

function dismiss_invitation(friend_id){
  $.post("dismiss_invitation",{"friend_id":friend_id});
}

function enter_room(){
  window.location.replace("guest_gameRoom/");
}


function join_room(friend_id){
  $.post("join_room",{"friend_id":friend_id})
  .done(function(data){
    $('#message_invitation').modal('hide');
    if(data.message != "") {
      $("#error_message_text").html(data.message);
      $("#error_message").modal("show");
    }
    else{
      enter_room();
    }
  });
}

$(document).ready(function (){
get_message();
$("#invitation_list").click(function(e){
  var context=$(e.target).attr("id");
  if (context.includes("join")) {
    var friend_id=context.replace("join-",'');
    join_room(friend_id);//navigate to room
    //$(e.target).text("joined!");

  };
  if (context.includes("dismiss")) {
    var friend_id=context.replace("dismiss-",'');
    dismiss_invitation(friend_id);
    $(e.target).parent().parent().hide();
  }
});

//window.setInterval(get_message, 5000);

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
      beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    });
})
