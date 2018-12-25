var roomNum = $("#room").attr("value");
var uesrID = $("#user").attr("value");
var startTime = new Date($("#time").attr("value"));

var webSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/racing/' + roomNum + '/' + uesrID + '/');

webSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data["message"];
    if(message == "score") {
        $('#score_' + data["user"]).html(data["text"])
        if(data["user"] == uesrID) {
            $("#coins").html(data["wallet"])
            $("#final_score").modal("show");
        }
    }
    else if(message == "move") {
        $('#race_' + data['user']).css('margin-left', data['text']);
    }
};

webSocket.onclose = function(e) {
    console.error('Web socket closed unexpectedly');
};

var spaceUp = true;

document.onkeydown = function(e) {
    if(spaceUp && (e.keyCode == 0 || e.keyCode == 32)) {
        e.preventDefault()
        var margin = parseInt($("#race_" + uesrID).css("margin-left").slice(0, -2), 10) + 10;
        if(margin <= 700) {
            webSocket.send(JSON.stringify({
                'message': 'move', 
                'text': margin + 'px', 
            }));
        }
        
        if(margin == 700) {
            var endTime = new Date();
            var score = parseInt((endTime - startTime) / 1000);
            var score_text = score + 's';
            webSocket.send(JSON.stringify({
                'message': 'score', 
                'text': score_text, 
                'score': score, 
            }));
        }
        spaceUp = false;
    }
}
document.onkeyup = function(e){
    if(e.keyCode == 0 || e.keyCode == 32) {
        spaceUp = true;
    }
}

function timer() {
    var time = parseInt((new Date() - startTime) / 1000);
    $('#second').html(('00' + time % 60).slice(-2));
    $('#minute').html(('00' + parseInt(time / 60)).slice(-2));
    if(time > 600) {
        $("#game_over").modal("show");
    }
}

window.setInterval(timer, 1000);

$(document).ready(function (){
    timer();
    $(".game_over_close").click(function(e){
        window.location.replace("/tamagochi/multiGame/instruction");
    })
});