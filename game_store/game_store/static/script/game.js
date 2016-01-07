/*global $, document, window, alert, Cookies*/

$(document).ready(function () {
    'use strict';

    function setting(options) {
        $('#game-iframe').attr('width', options.width);
        $('#game-iframe').attr('height', options.height);
    }

    function score(scr) {
        //build post data
        var post_data = {
            game: $('#game-iframe').data('game-id'),
            score: scr,
            csrfmiddlewaretoken: Cookies.get('csrftoken')
        };
        //Send POST ajax request to update the score
        $.post("/ajax/score", post_data)
            .done(function () {
                $('#game-info-alert').html("Score Submitted!");
                $('#game-info-alert').show().delay(5000).hide(0);
            })
            .fail(function () {
                $('#game-errors-alert').show();
                //Click handler for error close button
                $('#game-errors-alert .close').click(function () {
                    $('#game-errors').html(""); //clear all the errors
                    $('#game-errors-alert').hide(); //hide the error div
                });
                $('#game-errors').append('<li>' + scr + '</li>');
            });
    }

    function save(gameState) {

    }

    function load_request() {

    }

    $(window).on('message', function (evt) {
        var message = evt.originalEvent.data;
        switch (message.messageType) {
        case "SETTING":
            setting(message.options);
            break;
        case "SCORE":
            score(message.score);
            break;
        case "SAVE":
            save(message.gameState);
            break;
        case "LOAD_REQUEST":
            load_request();
            break;
        }
    });

});
