function search_friend(name) {
  //console.log(name);
  $.get("search_friend/"+name)
  .done(function(data){
    var list = $("#search-result");
    list.html('');
    for (var i=0; i<data.friends.length; i++) {
      friend=data.friends[i];
      var new_friend=$(friend.html);
      new_friend.data("friend-id", friend.id);
      list.prepend(new_friend);
    }
  })
}

function near_friend() {
  //console.log(name);
  $.get("near_by")
  .done(function(data){
    console.log("ee")
    var list = $("#nearby-result");
    list.html('');
    for (var i=0; i<data.friends.length; i++) {
      friend=data.friends[i];
      var new_friend=$(friend.html);
      new_friend.data("friend-id", friend.id);
      list.prepend(new_friend);
    }
  })
}

function invite_friend(friend_id){
  $.post("invite_friend",{"friend_id":friend_id});
}

function approve_friend(friend_id){
  $.post("approve_friend",{"friend_id":friend_id});
}

function dismiss_friend(friend_id){
  $.post("dismiss_friend",{"friend_id":friend_id});
}

function populate_friend(){
  $.get("get_friend")
  .done(function(data){
    var list=$("#myfriendlist");
    list.html('');
    for (var i=0; i<data.friends.length; i++) {
      friend=data.friends[i];
      var new_friend=$(friend.html);
      new_friend.data("friend-id", friend.id);
      list.prepend(new_friend);
    }
  })
}

function update_friendwaitlist(){
    $.get("get_friendwaitlist")
    .done (function(data){
      var number=$("#friend_waitlist_number");
      number.html('');
      waitlist_number=data.waitlist_number;
      number.prepend(waitlist_number);
      var waitlist=$("#waitlist");
      waitlist.html('');
      for (var i=0; i<data.friends.length; i++) {
        friend=data.friends[i];
        var new_friend=$(friend.html);
        new_friend.data("friend-id", friend.id);
        waitlist.prepend(new_friend);
      }
    });
}


$(document).ready(function (){
  $("#search-btn").click(function(){
    var name=document.getElementById("search-field").value;
    search_friend(name);
  });
  $("#search-field").keypress(function (e) {
    if (e.which == 13)
    var name=document.getElementById("search-field").value;
    search_friend(name);
  } );

  $("#search-result").click(function(e){
    var context=$(e.target).attr("id");
    console.log(context)
    if (context.includes("invite")) {
      var friend_id=context.replace("invite-",'');
      invite_friend(friend_id);
      $(e.target).parent().hide();
    }
  });

  $("#nearby-result").click(function(e){
    var context=$(e.target).attr("id");
    console.log(context)
    if (context.includes("invite")) {
      var friend_id=context.replace("invite-",'');
      invite_friend(friend_id);
      $(e.target).parent().hide();
    }
  });

$("#waitlist").click(function(e){
  var context=$(e.target).attr("id");
  if (context.includes("approve")) {
    var friend_id=context.replace("approve-",'');
    approve_friend(friend_id);
    $(e.target).text("Approved!");
  };
  if (context.includes("dismiss")) {
    var friend_id=context.replace("dismiss-",'');
    dismiss_friend(friend_id);
    $(e.target).parent().hide();
  }
});

  populate_friend();
  update_friendwaitlist();
  near_friend();

window.setInterval(populate_friend, 5000);
window.setInterval(update_friendwaitlist, 5000);

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
