$(function () {
    $('a[href*="#"]:not([href="#"])').click(function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html, body').animate({
                    scrollTop: target.offset().top
                }, 1000);
                return false;
            }
        }
    });
    var mq = window.matchMedia("(min-width: 666px)");

    if (mq.matches) {
        var vid = document.getElementById("bgvid");
        vid.play();
    }
    $("#owl-example").owlCarousel({dots: true, items: 1, itemsMobile: [666, 1]});
    //$(window).scroll(function (event) {
    //    event.preventDefault();
    //    $('html, body').animate({
    //        scrollTop: $(window).scrollTop()+5
    //    }, 1000);
    //
    //});
    $('#contact').submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: '/api/v1/message/',
            method: "POST",
            data: JSON.stringify({
                email:$('#email').val(),
                text:$('#message').val()
            }),
            contentType:'application/json',
            success: function(result) {
                console.log("sent the email: " + result);
                $('form.contact').replaceWith('<div class="content contact response">' + "We will contact you within 24 hours" + '</div>');
            },
            error: function() {
                alert('error!');
            }
        });
    });
/*    $('#login').submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: '/api/v1/owner/login/',
            method: 'POST',
            data: JSON.stringify({
                username:$('#username').val(),
                text:$('#message').val()
            }),
            contentType:'application/json',
            success: function(result) {
            },
            error: function() {
                alert('error!');
            }
        });
    }); */

}); 
