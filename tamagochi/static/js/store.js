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

$(document).ready(function (){
    $(".addbtn").click(function(e) {
        $.ajax({
            url: "/tamagochi/add_item",
            type: "POST",
            data: {
                item: $(this).attr("id"), 
                csrfmiddlewaretoken: getCSRFToken('csrftoken'),
            }, 
            dataType: "json",
            success: function(response){
                if('success' in response){
                    $("#shoppingCartList").append(response['success']);
                    var currentPrice = parseInt($("#total_price").text(),10);
                    currentPrice = currentPrice + response['price'];
                    $("#total_price").text(currentPrice);

                    $(".minusbtn").last().click(function(e) {
                        var currentPrice = parseInt($("#total_price").text(),10);
                        currentPrice = currentPrice - response['price'];
                        $("#total_price").text(currentPrice);
                        $(this).parent().parent().parent().remove();
                    });
                }
            }
        });
    });
    
    $("#order").click(function(e) {
        if(parseInt($("#total_price").text(),10) <=  parseInt($("#wallet").text(),10)) {
            var data = {
                items : [], 
                csrfmiddlewaretoken: getCSRFToken('csrftoken'),
            }

            $(".shoppingCartList").each(function(e) {
                data.items.push($(this).attr("id"));
            });

            $.ajax({
                url: "/tamagochi/order_item",
                type: "POST",
                data: data, 
                dataType: "json",
                success: function(response) {
                    if('success' in response) {
                        location.reload();
                    }
                }
            });
        }
        else if($("#shoppingCartList").find(".error").length == 0) {
            if(document.getElementById("errormsg").innerHTML === "") {
                $("#errormsg").prepend($("<p class='error'>You don't have enough money!</p>"))
            }
        }
    });
})