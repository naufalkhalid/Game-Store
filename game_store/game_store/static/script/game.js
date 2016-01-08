/*global $, document, window, alert, Cookies*/

$(document).ready(function () {
    'use strict';

    function show_message(type, message) {
        if (type === 'success') {
            $('#game-info-alert').html(message);
            $('#game-info-alert').show().delay(5000).hide(0);
        } else if (type === 'error') {
            $('#game-errors-alert').show();
            //Click handler for error close button
            $('#game-errors-alert .close').click(function () {
                $('#game-errors').html(""); //clear all the errors
                $('#game-errors-alert').hide(); //hide the error div
            });
            $('#game-errors').append('<li>' + message + '</li>');
        }
    }

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
                show_message('success', 'Score added to score board');
            })
            .fail(function (data) {
                show_message('error', data.responseText);
            });
    }

    function save(gameState) {
        //Building POST data
        var post_data = {
            game: $('#game-iframe').data('game-id'),
            state: JSON.stringify(gameState),
            csrfmiddlewaretoken: Cookies.get('csrftoken')
        };
        //Send POST ajax request to save game state
        $.post("/ajax/state", post_data)
            .done(function () {
                show_message('success', 'Game saved');
            })
            .fail(function (data) {
                show_message('error', data.responseText);
            });
    }

    function load_request() {
        //Building GET data
        var get_data = {
            game: $('#game-iframe').data('game-id')
        };
        //Send GET ajax request to get game state
        $.get("/ajax/state", get_data)
            .done(function (data) {
                show_message('success', 'Game loaded');
                var msg = {
                    "messageType": "LOAD",
                    "gameState": JSON.parse(data)
                };
                document.getElementById('game-iframe').contentWindow.postMessage(msg, "*");
            })
            .fail(function (data) {
                show_message('error', data.responseText);
                var msg =  {
                    messageType: "ERROR",
                    info: data.responseText
                };
                document.getElementById('game-iframe').contentWindow.postMessage(msg, "*");
            });
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
