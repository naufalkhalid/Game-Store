/*global $, document, window, alert*/

$(document).ready(function () {
    'use strict';

    function setting(options) {
        $('#game-iframe').attr('width', options.width);
        $('#game-iframe').attr('height', options.height);
    }

    function score(scr) {

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
