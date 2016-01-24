$(document).ready(function(){

$("#btn_Delgame").click(function(){

$("#dialog-del-message-Model").modal("show");

});

$("#btnSRDelYes").click(function(){
	
	var get_data = {
            game: $('#btnSRDelYes').data('game-id')
        };
        //Send GET ajax request to get game state
        $.get("/edit_game/"+get_data.game,get_data)
            .done(function (data) {
                
              alert(data);
			  window.location.href="/dashboard"
            })
            .fail(function (data) {
               alert("Failure"); 
            });
    
	
	
});
	
	
	
	
});