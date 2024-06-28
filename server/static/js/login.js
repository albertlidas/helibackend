$(function () {
    $('#login').submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: '/api/v1/owner/login/',
            method: 'POST',
            data: JSON.stringify({
                username:$('#username').val(),
                password:$('#password').val()
            }),
            contentType:'application/json',
            success: function(result) {
                console.log('token: ' + result.token);
                localStorage['owner_token'] = result.token;
                localStorage['owner'] = JSON.stringify(result);
                window.location.replace('/manager/');
            },
            error: function() {
                alert('error!');
            }
        });
    });
    
    $("#sign-up").click(function() {
        window.location = '/signup/';
    });
});
