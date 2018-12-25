function populateList() {
    $.get("get_post")
      .done(function(data) {
          var list = $("#post-list");
          list.html('');
          for (var i = 0; i < data.posts.length; i++) {
              post = data.posts[i];
              var new_post = $(post.html);
              list.prepend(new_post);
          }
      });
}


function addPost(){
    var postField = $("#post-field");
    $.post("add_post", {"post": postField.val()})
      .done(function(data) {
          populateList();
          postField.val("").focus();
      });
}

function addAgree(post_id) {
  $.post("agree_post",{"post_id":post_id});
  populateList();

}


$(document).ready(function () {
  // Add event-handlers
  $("#post-btn").click(addPost);
  $("#post-field").keypress(function (e) { if (e.which == 13) addPost(); } );

  // Set up to-do list with initial DB items and DOM data
  populateList();
  $("post-field").focus();
  $("#post-list").click(function(e){
      var id=$(e.target).attr("id");
      if (id.includes("agree")){
        var post_id=id.replace('agree-','');
        addAgree(post_id);
      };
    })
  // Periodically refresh to-do list
  window.setInterval(populateList, 1000);

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
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
})
