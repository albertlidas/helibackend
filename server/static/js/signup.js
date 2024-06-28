$(function() {
    $( document ).ready(function() {
    });
    $('#registration').submit(function (e) {
        e.preventDefault();
        if ($('#password').val() == $('#confirm-password').val()) {
            var profile = { country: $('#country').val(), city: $('#city').val(), address: $('#address').val(),
                            contact_name: $('#contact').val(), phone: $('#phone').val(), organization: $('#company').val()};
            $.ajax({
                url: '/api/v1/owner/create/',
                method: 'POST',
                data: JSON.stringify({
                    username:$('#email').val(),
                    email:$('#email').val(),
                    password:$('#password').val(),
                    profile: profile
                }),
                contentType:'application/json',
                success: function(result) {
                    console.log('registration: ' + JSON.stringify(result));
//                    localStorage['owner_token'] = result.token;
//                    window.location.replace('/manager/');
					$.ajax({
			            url: '/api/v1/owner/login/',
			            method: 'POST',
			            data: JSON.stringify({
			                username:$('#email').val(),
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
                },
                error: function(e) {
	                console.log(e);
                    alert('error!');
                }
            });
        }
    });
    $("#sign-in").click(function() {
        window.location = '/login/';
    });
});
