function check_status(){
  $.get("check_status")
  .done(function(data){
    var message_box=$("#message_box");
    message_box.html('');
    var new_message="<p>"+data.message+"</p>";
    message_box.append(new_message);
    var game_status=data.game_status;
    var pet_id=data.pet_id;
    console.log(game_status,pet_id)
    if (game_status=="Ready") {
      open_room_btn="<a href='/tamagochi/gameroom/'><button class='btn-success text-center hvr-buzz'><p>open a room</p></button></a>"
      message_box.append(open_room_btn);
    }
  });
};


function display_online_friends(){
  $.get("get_online_friends")
  .done(function(data){
   var list=$("#online_friend_list");
   console.log(data)
   list.html("");
   for (i=0;i<data.friends.length;i++) {
     var friend=data.friends[i];
     var new_friend=$(friend.html6);
     list.append(new_friend);
   }
  });
}

function invite_friend_play(friend_id){
  $.post("invite_friend_play",{"friend_id":friend_id});
}


$(document).ready(function (){
  $("#check_status").click(check_status);
  $("#invite_player-btn").click(display_online_friends);
  $("#online_friend_list").click(function(e){
    var context=$(e.target).attr("id");
    if (context.includes("invite")) {
      var friend_id=context.replace("invite-",'');
      invite_friend_play(friend_id);
      $(e.target).parent().hide();
    }
  });


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
