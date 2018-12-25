var td = Array();
			var playing = false;
			var score = 0;
			var beat = 0;
			var success = 0;
			var knock = 0;
			var countDown = 30;
			var interId = null,
				timeId = null;

			function GameOver(){
				timeStop();
				playing = false;
				clearMouse();
				alert("Game Over！\nYour Score is："+score+"\nYour Hit Rate is："+success+"\n Congrats! You win "
					+score+" coins!!!");
				TransportScore(score);
				success = 0;
				score = 0;
				knock = 0;
				beat = 0;
				countDown = 30;
			}

			function TransportScore(score){
				$.post("score2", {"score": score})
			}
			function timeShow(){
				document.form1.remtime.value = countDown;
				if(countDown === 0)
					{
						GameOver();
					}
				else
					{
						countDown = countDown-1;
						timeId = setTimeout("timeShow()",1000);
					}
			}

			function timeStop(){
				clearInterval(interId);
				clearTimeout(timeId);
			}

			function clearMouse(){
				for(var i=0;i<=24;i++)
				{
					document.getElementById("td["+i+"]").innerHTML="";
				}
			}

			function hit(id){
				if(playing===false)
				{
					alert("Click the start button to start the game!");
				}
				else
				{
					 beat +=1;
					if(document.getElementById("td["+id+"]").innerHTML!=="")
					{
						score += 1;
						knock +=1;
						success = knock/beat;
						document.form1.success.value = success;
						document.form1.score.value = score;
						document.getElementById("td["+id+"]").innerHTML="";
					}
					else
					{
						score += -1;
						success = knock/beat;
						document.form1.success.value = success;
						document.form1.score.value = score;
					}
				}
			}
