$(function() {

    var getLocation =  function(address, callback) {

        var geocoder = new google.maps.Geocoder();
        geocoder.geocode( { 'address': address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                var latitude = results[0].geometry.location.lat();
                var longitude = results[0].geometry.location.lng();
                console.log('coordinates: ' + latitude, longitude);
                // var coords = {latitude: latitude, longitude: longitude};
                // return {latitude: latitude, longitude: longitude};
                callback({latitude: latitude, longitude: longitude});
                // return coords;
            }
            console.log('maps are fucked');
            return undefined;
        }); 

    }

    function formatDate(date) {
        return moment.utc(date).format('DD/MM/YYYY HH:mm a');
    }

    var showSchedules = function () {
       console.log('show schedules for active route');
       var $elements = $('div.route.active').nextUntil('div.route').filter('div.schedule-detail');
       showSchedulesWithAnimation($elements);
    }
    
    var hideSchedules = function () {
       console.log('hide schedules for active route');
       var $elements = $('div.route.active').nextUntil('div.route').filter('div.schedule-detail');
       hideSchedulesWithAnimation($elements);
    }
    
    var showSchedulesWithAnimation = function ($elements){
	    if (!$elements) return;
	    $elements.show();
	    //  $($elements).css('height', "auto"); // Possible bug fix
	    var elementsHeight = $($elements).height();
	    $($elements).css('height', 0);
	    $elements.animate({height: elementsHeight}, 150);
    }
    
    var hideSchedulesWithAnimation = function ($elements){
	    var elementsHeight = $($elements).height();  
	    $elements.animate({height: 0}, 150, function(){
	      $elements.hide();
	      $($elements).css('height', elementsHeight);
	    });
    }

    var processRoutes = function() {
        $.ajax({
            url: '/api/v1/routes/',
            method: 'GET',
            headers: {
                'Authorization': 'Token '+ localStorage['owner_token']
            },
            contentType:'application/json',
            success: function(result) {
                if ( result && ( 0 < result.length)) {
                    for ( var i = 0; i < result.length; i++) {
//                        console.log('result[' + i + ']: ' + JSON.stringify(result[i]));
                        var route = '<div class="route" data-id="' + result[i].id + '"><div class="route-endings">' +
                                    result[i].starting_point + '&nbsp;-&nbsp;' + result[i].destination_point +
                                    '</div>' +
                                    '<div class="route-active-controls">' +
                                    ' <div class="route-line"></div>' +
                                    '<div class="route-active-controls-new">' +
                                    '<i class="glyphicon glyphicon-plus-sign"></i>&nbsp;Add new</div>' +
                                    '<div class="route-active-controls-close"><i class="glyphicon glyphicon glyphicon-remove"></i>&nbsp;Remove</div>' +
                                    '</div>' +
                                    '</div>';
                        $('.routes-container').append(route);
                        processSchedules(result[i].id);
                    }
//                    $('div.route').first().addClass('active');
                }
            },
            error: function() {
                alert('error!');
            }
        });
    };

    var fillModels = function() {
        $.ajax({
            url: '/api/v1/helicopters/',
            method: 'GET',
            headers: {
                'Authorization': 'Token '+ localStorage['owner_token']
            },
            contentType:'application/json',
            success: function(birds) {
                for (var i = 0; i < birds.length; i++) {
	                var vesselModel = $('#vessel-model')
	                vesselModel.change(function (arg){
		                 $('#seats').val($(this.options[this.selectedIndex]).attr('seats'));
		            });
                    vesselModel.append($('<option selected></option>').attr({
                        'value': birds[i].id, 'seats': birds[i].seats_count.toString()
                    }).text(birds[i].title));
                    $('#seats').val(birds[i].seats_count.toString());
                };
            },
            error: function() {
                alert('error!');
            }
        });
    };


  var processSchedules = function(routeID) {
        $.ajax({
            url: '/api/v1/departures/' + routeID + '/',
            method: 'GET',
            headers: {
                'Authorization': 'Token '+ localStorage['owner_token']
            },
            contentType:'application/json',
            success: function(departures) {
//                console.log('departures: ' + JSON.stringify(departures));
                if ( departures && ( 0 < departures.length)) {
                    var template = '';
                    for ( var j = 0; j < departures.length; j++) {
                        var availableSeats = 0;
                        departures[j].seats.forEach(function(seat, index, array) {
							!seat.passenger && ++availableSeats;
						});
						
                        template  += '<div class="schedule-detail" data-id="' + departures[j].departure_id + '" data-image="' + departures[j].helicopter.image + '">' +
                             '<div class="schedule-detail-top">' +
                             '&#35;' + departures[j].board + '&nbsp;' + departures[j].helicopter.title + '<br>' +
                             'Departure ' + formatDate(departures[j].departure_time) +
                             ' - Arrival ' + formatDate(departures[j].arrival_time) +
                             '</div>' +
                             '<div class="schedule-detail-bottom">' +
                             '<div class="schedule-detail-bottom-left">' +
                             availableSeats + ' of ' + departures[j].helicopter.seats_count + ' seats available' +
                             '</div>' +
                             '<div class="schedule-detail-bottom-right">$' + departures[j].ticket_cost + ' USD</div>' +
                             '<div class="schedule-detail-bottom-middle"><i class="glyphicon glyphicon glyphicon-remove"></i>&nbsp;Remove</div>' +
                             '</div>' +
                             '</div>';
                    }
//                    console.log("built schedules for route: " + routeID);
                    var currentRoute = $('.route[data-id=' + routeID + ']');
                    $(currentRoute).after(template);
                    if($(currentRoute).hasClass("active")) showSchedules();
                }
            },
            error: function() {
                alert('error!');
            }
        });
    }

    var initDashboardInfo = function () {
	   // company-label
	   var owner = localStorage['owner'];
	   if(owner)
	   {
		   owner = JSON.parse(owner);
		   $(".company-label").append("Company: "+owner.organization);
	   }
	   console.log(localStorage['owner']);
    }

    $( document ).ready(function() {
        // for now, just check that the token is present
        // we need a proper validation XXX!!!
        if (!localStorage['owner_token'] || ('' == localStorage['owner_token'])) window.location.replace('/login/');

        initDashboardInfo();
        // $.when(processRoutes(), $('div.route.active').next('div.schedule-detail').show());
        processRoutes();
        fillModels();
    });
    
    function blurElement(element, size) {
     var filterVal = 'blur(' + size + 'px)';
     $(element)
         .css('filter', filterVal)
         .css('webkitFilter', filterVal)
         .css('mozFilter', filterVal)
         .css('oFilter', filterVal)
         .css('msFilter', filterVal)
         .css('transition', 'all 0.2s ease-out')
         .css('-webkit-transition', 'all 0.2s ease-out')
         .css('-moz-transition', 'all 0.2s ease-out')
         .css('-o-transition', 'all 0.2s ease-out');
    }

    var showPassengerInfoWithAnimation = function (passengerInfo){
	    $(passengerInfo).css('height', $(passengerInfo).height());
		$(passengerInfo).find('.right-seat-reserved-top').hide();
		$(passengerInfo).find('.right-seat-name').show();
		$(passengerInfo).find('.right-seat-reserved').show();
	    $(passengerInfo).animate({height:"158px"}, 150);
    }

    var hidePassengerInfoWithAnimation = function (passengerInfo){
	    $(passengerInfo).css('height', $(passengerInfo).height());
	    $(passengerInfo).find('.right-seat-name').hide();
		$(passengerInfo).find('.right-seat-reserved').hide();
	    $(passengerInfo).animate({height: "40px"}, 150, function(){ $(passengerInfo).find('.right-seat-reserved-top').show();});
    }

    var showActiveRouteWithAnimation = function (route){
	    $(route).css('height', $(route).height());
	    $(route).animate({height:"121px"}, 150);
		$(route).addClass('active');
    }
    
    var hideActiveRouteWithAnimation = function (route){
	    $(route).css('height', $(route).height());
	    $(route).animate({height: "65px"}, 150);
    }

    var showRouteAddPopup = function () {
	    $('div.popup-route-add').show();
	    blurElement('div.page-section', 5);
    }

    var hideRouteAddPopup = function () {
	    $('div.popup-route-add').hide();
	    $('#origin').val("");
	    $('#origin-lat').val("");
	    $('#origin-long').val("");
	    $('#target').val("");
	    $('#target-lat').val("");
	    $('#target-long').val("");
	    blurElement('div.page-section', 0);
    }

    var showScheduleAddPopup = function () {
	    $('div.popup-schedule-add').show();
	    blurElement('div.page-section', 5);
    }

    var hideScheduleAddPopup = function () {
	    $('#board').val("");
	    $('#pilot1').val("");
	    $('#pilot2').val("");
	    $('#price').val("");
	    $('#information').val("");
	    $('div.popup-schedule-add').hide();
	    blurElement('div.page-section', 0);
    }

    var hideInfo = function () {
	    $('div.main-view-header').hide();
        $('div.main-view-body').hide();
        $('div.right-rail').empty();
    }

    var processingOfRightSeatAppearance = function (seatObject){
		var clickedSeat = $(seatObject).hasClass('right-seat') ? $(seatObject) : $(seatObject).parents('.right-seat').first();
        if (clickedSeat.hasClass('maximized'))
        {
	        //hide active seat;
	        setTimeout(function() {
		        hidePassengerInfoWithAnimation(clickedSeat);
		        clickedSeat.removeClass('maximized');
			}, 10);

			return;
	    }

	    setTimeout(function() {
		    clickedSeat.addClass("maximized");
		    showPassengerInfoWithAnimation(clickedSeat);
		}, 10);
	}

    $('body').on('click', 'div.vessel-seat-container', function(e) {
	    console.log('detected click on div.vessel-seat-container');
	    console.log(e);
	    var clickedSeat = $(e.target).hasClass('vessel-seat-container') ? $(e.target) : $(e.target).parents('.vessel-seat-container').first();
	    if(clickedSeat)
	    {
		    var seatNumber = clickedSeat.attr('data-id');
		    var seatInfo = $("div.right-seat[data-id='" + seatNumber + "']");
		    if(seatInfo && seatInfo.length > 0)
		    {
			    processingOfRightSeatAppearance(seatInfo.first());
		    }
	    }
	});

    $('body').on('click', 'div.right-seat', function(e) {
	    console.log('detected click on div.right-seat');
	    processingOfRightSeatAppearance(e.target);
	});

    $('body').on('click', 'div.route', function(e) {
        console.log('detected click on div.route');
        hideInfo();
        var $el = $('div.route.active');

        if ((0 < $(e.target).parents('div.route.active').length) || $(e.target).hasClass('active')) 
        {
	        //hide active route and schedules;
	        setTimeout(function() {
		        hideActiveRouteWithAnimation($el);
		        hideSchedules();
		        $el.removeClass('active');
			}, 100);
			
			return;
	    }
        console.log('detected click on inactive route');
        
        setTimeout(function() {
	        hideActiveRouteWithAnimation($el);
            $el.removeClass('active');
            while ($el.next('div.schedule-detail').length) {
                $el = $el.next('div.schedule-detail');
                hideSchedulesWithAnimation($el);
            }
            
            var clickedRoute = $(e.target).hasClass('route') ? $(e.target) : $(e.target).parents('.route').first();
            showActiveRouteWithAnimation(clickedRoute);
            showSchedules();
        }, 100);
    });
    
    $('body').on('click', 'div.left-top-controls-new', function(e) {
        console.log('clicked add route');
        showRouteAddPopup();
    });

    $('body').on('click', 'div.route-active-controls-new', function(e) {
        console.log('clicked add schedule');
        e.stopPropagation(e);
        var $el = $(e.target);
        if (!$el.hasClass('route'))
            $el = $el.parents('div.route').first();
        console.log('clicked on route: ' + $el.attr('data-id'));
        $('#route-id').val($el.attr('data-id'));
        showScheduleAddPopup();
    });

    $(document).keydown(function(e){
		var code = e.keyCode || e.which;
		if (code == 27) { // escape key maps to keycode `27`
	        hideRouteAddPopup();
	        hideScheduleAddPopup();
		}
    });

	$('body').on('click', '.popup-route-add', function(e) {
		hideRouteAddPopup();
	});

	$('body').on('click', '.new-route', function(e) {
		e.stopPropagation(e);
	});

	$('body').on('click', '.popup-schedule-add', function(e) {
		hideScheduleAddPopup();
	});

	$('body').on('click', '.new-schedule', function(e) {
		e.stopPropagation(e);
	});

    $('body').on('click', '.popup-route-add-close', function() {
        hideRouteAddPopup();
    });

    $('body').on('click', '.popup-schedule-add-close', function() {
        hideScheduleAddPopup();
    });

       // clicked on the schedule detail panel
    $('body').on('click', 'div.schedule-detail', function(e) {

        $el = $(e.target);
        if (!$el.hasClass('schedule-detail'))
            $el = $el.parents('div.schedule-detail').first();

        var routeID = $el.prevAll('div.route').first().attr('data-id');
        var scheduleID = $el.attr('data-id');
        var image = $el.attr('data-image');

        // get seats for my schedule
        $.ajax({
            url: '/api/v1/departures/' + routeID + '/',
            method: 'GET',
            headers: {
                'Authorization': 'Token '+ localStorage['owner_token']
            },
            contentType:'application/json',
            success: function(departures) {
                console.log('departures: ' + JSON.stringify(departures));
                if ( departures && ( 0 < departures.length)) {
                    var template = '';
                    for ( var j = 0; j < departures.length; j++) {
                        if (departures[j].departure_id == scheduleID) {
                            var seats = (departures[j].seats).sort(function(a, b){
                                            return a.seat - b.seat;
                                        });
//                            console.log('seats: ' + JSON.stringify(seats));
                            $('.main-view-header-vessel-schedule').text('#' + departures[j].board);
                            $('.main-view-header-vessel-model').text(departures[j].helicopter.title);
                            $('.main-view-header-pilots-first-name').text(departures[j].pilot1);
                            $('.main-view-header-pilots-second-name').text(departures[j].pilot2);
                            for ( var i = 0; i < seats.length; i++) {
                                template  += '<div class="right-seat" data-id="' + seats[i].seat + '">' +
                                     '<div class="right-seat-place">SEAT ' + seats[i].seat + '</div>' +
                                     '<div class="right-seat-reserved-top"><i class="glyphicon glyphicon-check"></i>&nbsp;' + 
                                     (seats[i].hasOwnProperty('passenger') ? 'Reserved' : 'Available') +
                                     '</div>' +
                                     '<div class="right-seat-name">' +
                                     (seats[i].hasOwnProperty('passenger') ? seats[i].passenger.first_name + ' ' + seats[i].passenger.last_name : '&nbsp;') +
                                     '</div>' +
                                     '<div class="right-seat-reserved"><i class="glyphicon glyphicon-check"></i>&nbsp;' + 
                                     (seats[i].hasOwnProperty('passenger') ? 'Reserved' : 'Available') +
                                     '</div>' +
                                     '</div>';
                            }
                            $('div.right-seat').remove();
                            $('div.right-rail').append(template);
                            $('.vessel-container').remove();
                            
                            var seatRows = '';
                            var seatsPerRow = 2;
                            for ( var j = 0; j < seats.length; j++) {
	                            if (j % seatsPerRow == 0) {
		                            if(seatRows.length > 0) seatRows += '</div>';
		                            seatRows += '<div class="vessel-seats-row">';
		                        }
		                        seatRows += '<div class="vessel-seat-container " data-id="' + seats[j].seat + '">';
		                        seatRows += '<img class='+(seats[j].passenger ? '"vessel-seat-occupied-image"' : '"vessel-seat-image"') + '>';	
		                        seatRows += '<div class="seat-badge">' + seats[j].seat + '</div>';                            
		                        seatRows += '</div>';
                            }
                            if(seatRows.length > 0) seatRows += '</div>';
                            
                            var helicopterContainer = 	'<div class="vessel-container">' +
                            								'<img src="' + image +'" class="vessel-image">' +
                            								'<div class="vessel-inner-container">' + seatRows + '</div>'+
                            							'</div>';
                            $('div.main-view-body').append(helicopterContainer);
                            $('div.main-view-header').show();
                            $('div.main-view-body').show();
                            return;
                        }
                    }
                }
            },
            error: function() {
                alert('error!');
            }
        });
    });
    
    $('body').on('click', 'div.right-top-controls-logout', function(e) {
        console.log('clicked sign-out');
        localStorage['owner_token'] = '';
        localStorage['owner'] = '';
        window.location.replace('/login/');
    });

    $('#add-route').submit(function (e) {
        e.preventDefault();
        getLocation($('#origin').val(), function(loc) {
            if (!loc) return;
            $('#origin-lat').val(loc.latitude);
            $('#origin-long').val(loc.longitude);
            getLocation($('#target').val(), function(loc) {
                if (!loc) return;
                $('#target-lat').val(loc.latitude);
                $('#target-long').val(loc.longitude);
                $.ajax({
                    url: '/api/v1/route/',
                    method: 'POST',
                    headers: {
                        'Authorization': 'Token '+ localStorage['owner_token']
                    },
                    data: JSON.stringify({
                        starting_point: $('#origin').val(),
                        destination_point: $('#target').val(),
                        latitude_start: $('#origin-lat').val(),
                        longitude_start: $('#origin-long').val(),
                        latitude_end: $('#target-lat').val(),
                        longitude_end: $('#target-long').val()
                    }),
                    contentType:'application/json',
                    success: function(result) {
//                        console.log('result: ' + JSON.stringify(result));
                         var route = '<div class="route" data-id="' + result.id + '"><div class="route-endings">' +
                                    result.starting_point + '&nbsp;-&nbsp;' + result.destination_point +
                                    '</div>' +
                                    '<div class="route-active-controls">' +
                                    ' <div class="route-line"></div>' +
                                    '<div class="route-active-controls-new">' +
                                    '<i class="glyphicon glyphicon-plus-sign"></i>&nbsp;Add new</div>' +
                                    '<div class="route-active-controls-close"><i class="glyphicon glyphicon glyphicon-remove"></i>&nbsp;Remove</div>' +
                                    '</div>' +
                                    '</div>';
                        var $el = $('div.route').last();
                        if (!$('div.route').length) 
                            $el = $('.left-top-controls');
                        if ($el.next('div.schedule-detail').length) 
                            $el = $el.next('div.schedule-detail');
//                        console.log("adding: " + route);
                        $el.after(route);
                        hideRouteAddPopup();
                    },
                    error: function() {
                        alert('error!');
                    }
                });
            });
        });
    });

    $('#add-schedule').submit(function (e) {
        e.preventDefault();
        var scheduleData = JSON.stringify({
                helicopter_id: $('#vessel-model').val(),
                ticket_cost: $('#price').val(),
                _time: $('#origin_time').val(),
                arrival_time: $('#target_time').val(),
                departure_time: $('#origin_time').val(),
                pilot1: $('#pilot1').val(),
                pilot2: $('#pilot2').val(),
                board: $('#board').val(),
                route: $('#route-id').val()});
        console.log("Add Schedule Data:", scheduleData);
                
        $.ajax({
            url: '/api/v1/departure/',
            method: 'POST',
            headers: {
                'Authorization': 'Token '+ localStorage['owner_token']
            },
            data: scheduleData,
            contentType:'application/json',
            success: function(result) {
                console.log('new schedule result: ' + JSON.stringify(result));
                var template = '<div class="schedule-detail" data-id="' + result.departure_id + '" data-image="' + result.helicopter.image + '">' +
                               '<div class="schedule-detail-top">' +
                               '&#35;' + result.board + '&nbsp;' + result.helicopter.title + '<br>' +
                               ' ' + formatDate(result.departure_time) + ' - ' +
                               'Arrival ' + formatDate(result.arrival_time) +
                               '</div>' +
                               '<div class="schedule-detail-bottom">' +
                               '<div class="schedule-detail-bottom-left">' +
                               result.helicopter.seats_count + ' of ' + result.helicopter.seats_count + ' seats available' +
                               '</div>' +
                               '<div class="schedule-detail-bottom-middle"><i class="glyphicon glyphicon glyphicon-remove"></i>&nbsp;Remove</div>' +
                               '<div class="schedule-detail-bottom-right">$' + result.ticket_cost + ' USD' + '</div>' +
                               '</div>';
                var $el = $('div.route.active').nextUntil('div.route').filter('div.schedule-detail').last();
                if (!$el.length) $el = $('div.route.active');
                $el.after(template);
                $el.next('div.schedule-detail').show();
                hideScheduleAddPopup();
            },
            error: function() {
                alert('error!');
            }
        });
    });

    $('body').on('click', 'div.schedule-detail-bottom-middle', function(e) {
        var scheduleID = $(e.target).parents('div.schedule-detail').first().attr('data-id');
        var result = confirm("Do you really want to delete?");
        if(result)
        {
	        $.ajax({
	            url: '/api/v1/departure/' + scheduleID + '/',
	            method: 'DELETE',
	            headers: {
	                'Authorization': 'Token '+ localStorage['owner_token']
	            },
	            data: JSON.stringify({}),
	            contentType:'application/json',
	            success: function(result) {
	                console.log('deleted schedule : ' + scheduleID);
	                $('div.schedule-detail[data-id="' + scheduleID + '"]').remove();
	            },
	            error: function() {
	                alert('error!');
	            }
	        });
        }
    });

    $('body').on('click', 'div.route-active-controls-close', function(e) {
	    e.stopPropagation(e);
        var routeID = $(e.target).parents('div.route').first().attr('data-id');
        var result = confirm("Do you really want to delete?");
		if(result)
		{
	        $.ajax({
	            url: '/api/v1/route/' + routeID + '/',
	            method: 'DELETE',
	            headers: {
	                'Authorization': 'Token '+ localStorage['owner_token']
	            },
	            data: JSON.stringify({}),
	            contentType:'application/json',
	            success: function(result) {
	                console.log('deleted route : ' + routeID);
	                $(e.target).parents('div.route').first().nextUntil('div.route').addBack().hide();
	            },
	            error: function() {
	                alert('error!');
	            }
	        });
        }
    });

});
