var roomNum = $("#room").attr("value");
var uesrID = $("#user").attr("value");
var owner = $("#owner").attr("value");
var startTime = new Date($("#time").attr("value"));

var webSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/room/' + roomNum + '/' + uesrID + '/');

function changeOwnerStatus() {
    var ready = 0;
    $(".player_status").each(function(index) {
        if($(this).text() == "Status: Ready!") {
            ready++;
        }
    })
    var number = $("#play_list").children().length;
    if(number <= ready+1) {
        $("#start-btn").prop('disabled', false);
    }
    else {
        console.log(number, ready);
        $("#start-btn").prop('disabled', true);
    }
    if(number >= 4) {
        $("#invite_player-btn").prop('disabled', true);
    }
    else {
        $("#invite_player-btn").prop('disabled', false);
    }
}
webSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data['message'];
    if(message == 'add' && $("#player_" + data['text']).length == 0) {
        $.ajax({
            url: "/tamagochi/get_player",
            type: "GET",
            data: {
                user_id: data['text'], 
            }, 
            dataType: "json",
            success: function(response){
                $("#play_list").append(response["success"]);
                changeOwnerStatus();
            }
        });
    }
    else if(message == "ready") {
        $("#status_" + data["text"]).html("Status: Ready!");
        changeOwnerStatus();
    }
    else if(message == "start") {
        window.location.replace("/tamagochi/multiGame/racing");
    }
};

webSocket.onclose = function(e) {
    console.error('Web socket closed unexpectedly');
};

function timer() {
    var time = 600 - parseInt((new Date() - startTime) / 1000);
    if(time <= 0) {
        webSocket.send(JSON.stringify({
            'message': 'timeup'
        }));
        $('#second').html('00');
        $('#minute').html('00');
        $("#time_up").modal("show");
    }
    else {
        $('#second').html(('00' + time % 60).slice(-2));
        $('#minute').html(('00' + parseInt(time / 60)).slice(-2));
    }
}

window.setInterval(timer, 1000);


$(document).ready(function (){
    changeOwnerStatus();
    $("#ready-btn").click(function(e) {
        webSocket.send(JSON.stringify({
            'message': 'ready'
        }));
    })
    $("#start-btn").click(function(e) {
        webSocket.send(JSON.stringify({
            'message': 'start'
        }));
    })

    timer();

    $(".time_up_close").click(function(e){
        window.location.replace("/tamagochi/multiGame/instruction");
    })
})
