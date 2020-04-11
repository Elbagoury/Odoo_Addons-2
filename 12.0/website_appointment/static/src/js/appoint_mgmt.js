/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('website_appointment.appoint_mgmt', function (require) {

    "use strict";
    var ajax = require('web.ajax');
    var core = require('web.core');

    function get_today_date(){
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth()+1; //January is 0!
        var yyyy = today.getFullYear();
        if(dd<10) {
            dd = '0'+dd
        }
        if(mm<10) {
            mm = '0'+mm
        }
        today = yyyy + '-' + mm + '-' + dd;
        return today
    }

    $(function () {
        $('.appoint_date_div').datetimepicker({
            format:'YYYY-MM-DD',
            pickTime: false,
            locale : moment.locale(),
            allowInputToggle: true,
            keyBinds: null,
            minDate: moment(),
            // calendarWeeks: true,
            // maxDate: moment().add(200, "d"),
            icons: {
                date: 'fa fa-calendar',
                next: 'fa fa-chevron-right',
                previous: 'fa fa-chevron-left',
            },
        });
    });

    $(document).ready(function(){

        $('#appoint_date').attr('min', get_today_date());
        $('#appoint_date').attr('value', get_today_date());

        $('tr.my_appointments_row').click(function() {
            var href = $(this).find("a").attr("href");
            if (href) {
                window.location = href;
          }
        });

        $('.appoint_groups , .appoint_date').on('change', function(){
            $('.appoint_person').empty()
            $('.appoint_person').append('<option value="" selected="1" disabled="1">--Select--</option>')
            var group_id = parseInt($("select.appoint_groups option:selected" ).val())
            var appoint_date = $('#appoint_date').val()
            if (!isNaN(group_id)){
                $('.appoint_loader').show();
                ajax.jsonRpc("/find/app/person", 'call', {
                    'group_id'  :   group_id,
                    'appoint_date': appoint_date,
                }).then(function(appoint_person_dict){
                    $.each(appoint_person_dict, function(key, value) {
                        $('.appoint_person').append($("<option></option>").attr("value",key).text(value));
                    });
                });
                $('.appoint_loader').hide();
            }
        });

        $('#appoint_date').on('input', function() {
        	var input=$(this);
        	var appoint_date=input.val();
        	if(appoint_date){$('#appoint_datetime_picker').removeClass("invalid").addClass("valid");
            }
        	else{$('#appoint_datetime_picker').removeClass("valid").addClass("invalid");}
        });

        $('#appoint_groups').on('input', function() {
        	var input=$(this);
        	var appoint_group=input.val();
        	if(appoint_group){
                input.removeClass("invalid").addClass("valid");}
        	else{input.removeClass("valid").addClass("invalid");}
        });

        // $('.appoint_groups , .appoint_date').on('change', function(){
        $('#button_find_appointee').on('click', function(event){
            event.preventDefault()
            var group_id =  parseInt($("select.appoint_groups option:selected" ).val())
            var appoint_date = $('#appoint_date').val()
            // var person_id =  parseInt($( "select.appoint_person option:selected" ).val())
            if (isNaN(group_id) && (appoint_date == '')){
                $('#appoint_groups').addClass("invalid");
                $('#appoint_datetime_picker').addClass("invalid");
            }
            else if (isNaN(group_id))
            {
                $('#appoint_groups').addClass("invalid");
            }
            else if (appoint_date == '') {
                $('#appoint_datetime_picker').addClass("invalid");
            }
            else{
                $('#appoint_groups').removeClass("invalid").removeClass("valid");
                $('#appoint_datetime_picker').removeClass("invalid").removeClass("valid");
                $('.appoint_loader').show();
                ajax.jsonRpc("/find/appointee/timeslot", 'call', {
                    'group_id'  :   group_id,
                    'appoint_date': appoint_date,
                    // 'person_id' :   person_id,
                }).then(function(appointee_listing_div){
                    if(appointee_listing_div == undefined){
                        $('#appoint_datetime_picker').addClass("invalid");
                        // alert("Appointment Date should be today or later.")
                        bootbox.alert({
                            title: "Warning",
                            message:"Appointment Date should be today or later.",
                        })
                    }
                    else{
                        $('div#appointee_listing').html(appointee_listing_div)
                    }
                });
                $('.appoint_loader').hide();
            }
        });

        // $('.appoint_person, .appoint_date, .appoint_groups').on('change', function(){
        //     $('div#appointee_listing').html('<div/>');
        // });

        function dateCompare(time1,time2) {
          var t1 = new Date();
          var parts = time1.split(":");
          t1.setHours(parts[0],parts[1],parts[2],0);
          var t2 = new Date();
          parts = time2.split(":");
          t2.setHours(parts[0],parts[1],parts[2],0);

          // returns 1 if greater, -1 if less and 0 if the same
          if (t1.getTime()>t2.getTime()) return 1;
          if (t1.getTime()<t2.getTime()) return -1;
          return 0;
        }


        $('#appointee_listing').on('click', '.button_book_now' , function(event){
            event.preventDefault()
            var $form = $(this).closest('form');

            // validate timeslot according to today date and time
            var appoint_date = new Date($('#appoint_date').val())
            var today = new Date()
            var res = -1

            if (appoint_date.getDate() == today.getDate() && appoint_date.getMonth() == today.getMonth() && appoint_date.getYear() == today.getYear() ){
                var h = today.getHours();
                var m = today.getMinutes();

                var t1 = h + ':' + m + ':' + '00'
                var start_time = $(this).parents('.appoint_timeslot_panel').find(".start_time").html()
                var parts = start_time.split(".");
                if (parts[0].length < 2){
                    parts[0] = '0' + parts[0]
                }
                if (parts[1].length < 2){
                    parts[1] = '0' + parts[1]
                }
                var t2 = parts[0] + ':' + parts[1] + ':' + '00'
                res = dateCompare(t1,t2);
            }

            if (res == 1 || res == 0){
                // alert("This slot is not available for today. Please select any other slot.")
                bootbox.alert({
                //   size: "small",
                  title: "Warning",
                  message: "This slot is not available for today. Please select any other slot.",
                })
            }
            else{
                var time_slot_id = parseInt($(this).parents('.appoint_timeslot_panel').first().attr('id'))
                $('#appointee_listing').append('<input type="hidden" name="appoint_timeslot_id" value="'+ time_slot_id + '" />');
                var person_id =  parseInt($( "select.appoint_person option:selected" ).val())
                var appoint_person_id = parseInt($(this).parents('.appoint_person_panel').first().attr('id'))

                // new code added for booking restriction
                ajax.jsonRpc("/check/multi/appointment", 'call', {
                    'appoint_date' : appoint_date,
                    'time_slot_id': time_slot_id,
                    'appoint_person_id': appoint_person_id,
                }).then(function(result){
                    if(result == false){
                        // alert("This slot is already booked for this person at this date. Please select any other.")
                        bootbox.alert({
                          title: "Warning",
                          message: "This slot is already booked for this person at this date. Please select any other.",
                        })
                    }
                    else{
                        $('#appointee_listing').append('<input type="hidden" name="appoint_timeslot_id" value="'+ time_slot_id + '" />');
                        if (isNaN(person_id)){
                            $('#appointee_listing').append('<input type="hidden" name="appoint_person" value="'+ appoint_person_id + '" />');
                        }
                        if(event.isDefaultPrevented()){
                            $form.submit();
                        }
                    }
                });
            }

        });

    });
});
