odoo.define('job_portal.job_portal', function (require) { 
    "use strict";

    var core = require('web.core');
    var odoo = require('web.ajax');
    var Dialog = require('web.Dialog');
    var rpc = require('web.rpc');
    var _t = core._t;
    var ajax = require('web.ajax');

    // For My profile page Models to create Applicant Details
    $(document).ready(function(){
          if($('.post_active').val()){
            $('.post-job-menu').css({"color":"rgba(0, 0, 0, 0.9)"})
        }
        $('.submit-job-definition').click(function(){
            var today_date=new Date()
            var selected_date=new Date($('.post_job_picker').val())

            if(today_date.getFullYear() > selected_date.getFullYear()){
                 alert("Please enter proper closing date")
                $('.post_job_picker').val("")
                return false
            }
            if (!parseInt(selected_date.getMonth())){
               alert("Please enter proper closing date")

                $('.post_job_picker').val("")
                return false
            }
            if (!parseInt(selected_date.getDate())){
                alert("Please enter proper closing date")
                $('.post_job_picker').val("")
                return false
            }
            if (!parseInt(selected_date.getFullYear())){
               alert("Please enter proper closing date")

                $('.post_job_picker').val("")
                return false
            }
            if (today_date > selected_date){
                alert("Please enter proper closing date")

                $('.post_job_picker').val("")
                return false
            }

            else{
            }
        })

        $('.post_job_picker').change(function(){
//            var t=new Date()
//            var selected_date=new Date($(this).val())
//            var dateformat = /^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$/;
//
//
//            if (t.getDate() > selected_date.getDate()){
//                alert("Please enter proper closing date")
//
//                $(this).val("")
//                return false
//            }
//
//            else{
//            }
        })
        $('.send-bio-data').click(function(){
            var flag=0;

            if($('.firstname-applicant').val()==''){
                $('.firstname-applicant').css({'border':'1px solid red'})
                flag=1;

            }
            if($('.middlename-applicant').val()==''){
                 $('.middlename-applicant').css({'border':'1px solid red'})
                 flag=1;

            }
            if($('.lastname-applicant').val()==''){
                 $('.lastname-applicant').css({'border':'1px solid red'})
                 flag=1;

            }
            if($('.gender-applicant').val()==''){
                 $('.gender-applicant').css({'border':'1px solid red'})
                 flag=1;

            }

            if($('.birthdate-applicant').val()==''){
                 $('.birthdate-applicant').css({'border':'1px solid red'})
                 flag=1;

            }
            if($('.birthdate-applicant').val()!=''){
                   var selected_date=new Date($('.birthdate-applicant').val())
            var curr_date=new Date()
            var diff=curr_date.getFullYear()-selected_date.getFullYear()
            if(diff>=100){
                 $('.birthdate-applicant').css({'border':'1px solid red'})
                 flag=1;
            }
            }
            if($('.marital-status-applicant').val()==''){
                 $('.marital-status-applicant').css({'border':'1px solid red'})
                 flag=1;

            }
            if($('.marital-status-applicant').val()==''){
                 $('.marital-status-applicant').css({'border':'1px solid red'})
                 flag=1;

            }
            if($('.mobile-applicant').val()==''){
                 $('.mobile-applicant').css({'border':'1px solid red'})
                 flag=1;

            }
              else if($('.mobile-applicant').val().match('^\d+$/')){
                    $('.mobile-applicant').css({'border':'1px solid red'})
                 flag=1;
                }
                     else if($('.mobile-applicant').val()<0){
             $('.mobile-applicant').css({'border':'1px solid red'})
                 flag=1;
         }

//            if($('.phone-applicant').val()==''){
//                 $('.phone-applicant').css({'border':'1px solid red'})
//                 flag=1;
//
//            }
            if($('.email-applicant').val()==''){
                 $('.email-applicant').css({'border':'1px solid red'})
                 flag=1;

            }
            if($('.street-applicant').val()==''){
                 $('.street-applicant').css({'border':'1px solid red'})
                 flag=1;

            }
            if($('.city-applicant').val()==''){
                 $('.city-applicant').css({'border':'1px solid red'})
                 flag=1;

            }
            if($('.zip-applicant').val()==''){
                 $('.zip-applicant').css({'border':'1px solid red'})
                 flag=1;

            }
            if($('.country-applicant').val()==''){
                 $('.country-applicant').css({'border':'1px solid red'})
                 flag=1;

            }
            if(flag==1){
                alert("Please fill all mandatory fields")
                return false;
            }
        })
        $('.birthdate-applicant').change(function(){
//            alert("change")
            var selected_date=new Date($(this).val())
            var curr_date=new Date()
            var diff=curr_date.getFullYear()-selected_date.getFullYear()
            if(diff<=12){
                alert("Please Select Proper Date")
                $(this).val("")
                return false;
            }
        })
        $('.jobportal_datepicker').datepicker({
            minDate:new Date(),
            icons: {
                time: "fa fa-clock-o",
                date: "fa fa-calendar",
                up: "fa fa-arrow-up",
                down: "fa fa-arrow-down"
            },
            format:'MM/DD/YYYY',
        });
        $(document).on('click', '#is_still', function(e){

            if ($(this).is(':checked')) {
                $(this).parents('.panel-body').find('.end_date_div').hide();
            } else {
                $(this).parents('.panel-body').find('.end_date_div').show();
            }
        });
        $('.country-applicant').change(function(){

             ajax.jsonRpc("/page/get_state_applicant", 'call', {
                    'country_id': $(this).find("option:selected").val()
                })
                .then(function(records) {
                 $('.state-applicant').find('option').remove()
                 $('.state-applicant')
         .append($("<option></option>")
                    .attr("value",'')
                    .text('--Select State--'));
                _.each(records, function(rec){
                  $('.state-applicant')
         .append($("<option></option>")
                    .attr("value",rec['id'])
                    .text(rec['name']));
                });

                })
        })

        $(".only_number").keypress(function (e) {
            if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
                return false;
           }
        });
        $(document).on('click', '.experience_btn', function(e){
            e.stopPropagation();
            e.preventDefault();
            $('#myModalExperience').modal();
            $('#myModalExperience').find("h4[class='modal-title']").text("Add Experience Details")
            $('#myModalExperience').find("input[name='operation_type']").val('insert')
            $('#myModalExperience').find('input,select,textarea').val('')
        });

        $(document).on('click', '#ExperienceEditModal', function(e){
            e.stopPropagation();
            e.preventDefault();
            var id = $(this).data('experience_id');
            var start_date_val = $(this).parents('tr').find('.exeperience_start_date').text();
            var end_date_val = $(this).parents('tr').find('.exeperience_end_date').text();
            $('#ExperienceEditModal'+id).modal();
            $('#ExperienceEditModal'+id).find("input[name='start_date']").val(start_date_val);
            $('#ExperienceEditModal'+id).find("input[name='end_date']").val(end_date_val);
        });
        $(document).on('click', '#AcademicEditModal', function(e){
            e.stopPropagation();
            e.preventDefault();
            var id = $(this).data('academic_id');
            var start_date_val = $(this).parents('tr').find('.academic_start_date').text();
            var end_date_val = $(this).parents('tr').find('.academic_end_date').text();
            $('#AcademicEditModal'+id).modal();
            $('#AcademicEditModal'+id).find("input[name='start_date']").val(start_date_val);
            $('#AcademicEditModal'+id).find("input[name='end_date']").val(end_date_val);
        });
        $(document).on('click', '#CertificationEditModal', function(e){
            e.stopPropagation();
            e.preventDefault();
            var id = $(this).data('certification_id');
            var start_date_val = $(this).parents('tr').find('.certification_start_date').text();
            var end_date_val = $(this).parents('tr').find('.certification_end_date').text();
            $('#CertificationEditModal'+id).modal();
            $('#CertificationEditModal'+id).find("input[name='start_date']").val(start_date_val);
            $('#CertificationEditModal'+id).find("input[name='end_date']").val(end_date_val);
        });
    });

    $(document).ready(function(){
      $('#top_menu li').addClass('job_portal_menus')
      $('.job_portal_menus').each(function(){

            if($.trim($(this).text())=='Post Job'){
                 $(this).attr('groups','base.group_erp_manager')
            }
      })
      $(document).on('click', '.certification_btn', function(e){
            e.stopPropagation();
            e.preventDefault();
            $('#myModalCertification').modal();
            $('#myModalCertification').find("h4[class='modal-title']").text("")
            $('#myModalCertification').find("h4[class='modal-title']").text("Add Certification Details")
            $('#myModalCertification').find("input[name='operation_type']").val('insert')
            $('#myModalCertification').find('input,select,textarea').val('')


        });
        $(document).on('click', '.academic_btn', function(e){
            e.stopPropagation();
            e.preventDefault();
            $('#myModalAcademic').modal();
            $('#myModalAcademic').find("h4[class='modal-title']").text("")
            $('#myModalAcademic').find("h4[class='modal-title']").text(" Add Academic Details")
            $('#myModalAcademic').find("input[name='operation_type']").val('insert')
            $('#myModalAcademic').find('input,select,textarea').val('')
        });


        /* affix the navbar after scroll below header */
        // Click event For Adding Academic of Applicants
        // Validation on the models can/should be improved later on
        $(document).on('click', '#add_academic', function(e){
            var current_val=new Date()
            var target = $(this).parents('#myModalAcademic');
            e.stopPropagation();
            e.preventDefault();

             var start_date_val=new Date(target.find("input[name='start_date']").val())
             var end_date_val=new Date(target.find("input[name='end_date']").val())
            if(target.find("input[name='operation_type']").val()=='update'){


            if(start_date_val>end_date_val){
                    alert("start date should not be greater than end date.")
                    return false
                }
                 if((start_date_val>=current_val)){
                    alert("start date  should not greater than or equal to today")
                    return false
                } if((end_date_val>=current_val)){
                    alert("end date should not greater than or equal to today")
                    return false
                }
            if ( $.trim(target.find("input[name='qualification']").val()) &&
                $.trim(target.find("input[name='study_field']").val()) &&
                $.trim(target.find("input[name='organization']").val()) &&
                $.trim(target.find("input[name='location']").val()) &&
                $.trim(target.find("input[name='start_date']").val()) &&
                $.trim(target.find("input[name='grade']").val())){

if($('#myModalAcademic').find("input[name='is_still']").is(":checked")){
                var qualification = target.find("input[name='qualification']").val()
                var study_field = target.find("input[name='study_field']").val()
                var organization = target.find("input[name='organization']").val()
                var location = target.find("input[name='location']").val()
                var start_date = target.find("input[name='start_date']").val()
                var is_still =  true
                var grade = target.find("input[name='grade']").val()
                var opr_id = target.find("input[name='opr_id']").val()
                  var tr_no = parseInt(target.find("input[name='tr_no']").val())+1
                   if ($('.academic_desc_table tr').length==2){
                        tr_no=1
                     }
                odoo.jsonRpc("/edit_academic_applicant", 'call', {
                    'qualification' : target.find("input[name='qualification']").val(),
                    'study_field' : target.find("input[name='study_field']").val(),
                    'organization' : target.find("input[name='organization']").val(),
                    'location' : target.find("input[name='location']").val(),
                    'start_date' : target.find("input[name='start_date']").val(),
                    'is_still' : true,
                    'grade' : target.find("input[name='grade']").val(),
                    'id' : target.find("input[name='opr_id']").val()
                }).then(function(rec) {
                     $(".academic_desc_table tr:eq("+$.trim(tr_no)+")").replaceWith("<tr><td>"+$.trim(target.find("input[name='qualification']").val()) +"</td><td>"+$.trim(study_field)+"</td><td>"+$.trim(organization)+"</td><td>"+$.trim(location)+"</td><td>"+$.trim(start_date)+"</td><td>"+$.trim(is_still)+"</td><td>"+$.trim(grade)+"</td><td><button type='button' class='btn edit_academic' data-toggle='modal' data-academic_id="+rec+"><i class='fa fa-pencil-square-o'></i></button><td><button type='button' data-academic_id="+rec+" class='btn delete_academic'><i class='fa fa-trash'></i></button></td></tr>")
                     $('#myModalAcademic').modal('hide')
                     $( "#academic_desc_table" ).load(window.location.href + " #academic_desc_table" );
//                    location.reload();
                });

}
else{
              var qualification =  target.find("input[name='qualification']").val()
              var study_field = target.find("input[name='study_field']").val()
              var organization = target.find("input[name='organization']").val()
              var location = target.find("input[name='location']").val()
              var start_date = target.find("input[name='start_date']").val()
              var end_date =  target.find("input[name='end_date']").val()
              var grade = target.find("input[name='grade']").val()
              var opr_id = target.find("input[name='opr_id']").val()
              var tr_no = parseInt(target.find("input[name='tr_no']").val())+1
                   if ($('.academic_desc_table tr').length==2){
                        tr_no=1
                     }
             odoo.jsonRpc("/edit_academic_applicant", 'call', {
                    'qualification' : target.find("input[name='qualification']").val(),
                    'study_field' : target.find("input[name='study_field']").val(),
                    'organization' : target.find("input[name='organization']").val(),
                    'location' : target.find("input[name='location']").val(),
                    'start_date' : target.find("input[name='start_date']").val(),
                    'end_date' : target.find("input[name='end_date']").val(),
                    'grade' : target.find("input[name='grade']").val(),
                    'id' : target.find("input[name='opr_id']").val()
                }).then(function(rec) {
                     $(".academic_desc_table tr:eq("+$.trim(tr_no)+")")
                     .replaceWith("<tr><td>"+$.trim(target.find
                     ("input[name='qualification']").val())+"</td><td>"+$
                     .trim(study_field)+"</td><td>"+$.trim(organization)
                     +"</td><td>"+$.trim(location)+"</td><td>"+$.trim(start_date)+"</td><td>"+$.trim(end_date)+"</td><td>"+$.trim(grade)+"</td><td><button type='button' class='btn edit_academic' data-toggle='modal' data-academic_id="+rec+"><i class='fa fa-pencil-square-o'></i></button><td><button type='button' data-academic_id="+rec+" class='btn delete_academic'><i class='fa fa-trash'></i></button></td></tr>")
                     $('#myModalAcademic').modal('hide')
//                    location.reload();\
                    $( "#academic_desc_table" ).load(window.location.href + " #academic_desc_table" );

                });
                }}
               else {
                Dialog.alert(self, _t("Please Give Proper Values to the Input fields !"), {
                    title: _t('Alert!'),
                });
            }
            }
            else if($.trim(target.find("input[name='operation_type']").val()=='insert'))
            {

                if(start_date_val>end_date_val){
                    alert("start date should not be greater than end date.")
                    return false
                }
                 if((start_date_val>=current_val)){
                    alert("start date  should not greater than or equal to today")
                    return false
                } if((end_date_val>=current_val)){
                    alert("end date should not greater than or equal to today")
                    return false
                }
                if ( $.trim(target.find("input[name='qualification']").val()) &&
                $.trim(target.find("input[name='study_field']").val()) &&
                $.trim(target.find("input[name='organization']").val()) &&
                $.trim(target.find("input[name='location']").val()) &&
                $.trim(target.find("input[name='start_date']").val()) &&
                $.trim(target.find("input[name='grade']").val())){


                if($('#myModalAcademic').find("input[name='is_still']").is(":checked")){
                    var qualification = target.find("input[name='qualification']").val()
                    var study_field = target.find("input[name='study_field']").val()
                    var organization = target.find("input[name='organization']").val()
                    var location = target.find("input[name='location']").val()
                    var start_date = target.find("input[name='start_date']").val()
                    var is_still =  true
                    var grade = target.find("input[name='grade']").val()
                      odoo.jsonRpc("/add_academic_applicant", 'call', {
                    'qualification' : target.find("input[name='qualification']").val(),
                    'study_field' : target.find("input[name='study_field']").val(),
                    'organization' : target.find("input[name='organization']").val(),
                    'location' : target.find("input[name='location']").val(),
                    'start_date' : target.find("input[name='start_date']").val(),
                    'is_still' : true,
                    'grade' : target.find("input[name='grade']").val(),
                }).then(function(rec) {
                    $('.academic_desc_table tr:last').after("<tr><td>"+$.trim(qualification)+"</td><td>"+$.trim(study_field)+"</td><td>"+$.trim(organization)+"</td><td>"+$.trim(location)+"</td><td>"+$.trim(start_date)+"</td><td>"+$.trim(is_still)+"</td><td>"+$.trim(grade)+"</td><td><button type='button' class='btn edit_academic' data-toggle='modal' data-academic_id="+rec+"><i class='fa fa-pencil-square-o'></i></button><td><button type='button' data-academic_id="+rec+" class='btn delete_academic'><i class='fa fa-trash'></i></button></td></tr>")
                    $('#myModalAcademic').modal('hide')
//                    location.reload();
$( "#academic_desc_table" ).load(window.location.href + " #academic_desc_table" );
                });

                 }
                 else
                 {
                    var qualification = target.find("input[name='qualification']").val()
                    var study_field = target.find("input[name='study_field']").val()
                    var organization = target.find("input[name='organization']").val()
                    var location = target.find("input[name='location']").val()
                    var start_date = target.find("input[name='start_date']").val()
                    var end_date =  target.find("input[name='end_date']").val()
                    var grade = target.find("input[name='grade']").val()
                odoo.jsonRpc("/add_academic_applicant", 'call', {
                    'qualification' : target.find("input[name='qualification']").val(),
                    'study_field' : target.find("input[name='study_field']").val(),
                    'organization' : target.find("input[name='organization']").val(),
                    'location' : target.find("input[name='location']").val(),
                    'start_date' : target.find("input[name='start_date']").val(),
                    'end_date' : target.find("input[name='end_date']").val(),
                    'grade' : target.find("input[name='grade']").val(),
                }).then(function(rec) {
                    $('.academic_desc_table tr:last').after("<tr><td>"+$.trim(qualification)+"</td><td>"+$.trim(study_field)+"</td><td>"+$.trim(organization)+"</td><td>"+$.trim(location)+"</td><td>"+$.trim(start_date)+"</td><td>"+$.trim(end_date)+"</td><td>"+$.trim(grade)+"</td><td><button type='button' class='btn edit_academic' data-toggle='modal' data-academic_id="+rec+"><i class='fa fa-pencil-square-o'></i></button><td><button type='button' data-academic_id="+rec+" class='btn delete_academic'><i class='fa fa-trash'></i></button></td></tr>")
                    $('#myModalAcademic').modal('hide')
                    //location.reload();
                    $( "#academic_desc_table" ).load(window.location.href + " #academic_desc_table" );
                });}
            } else {
                Dialog.alert(self, _t("Please Give Proper Values to the Input fields !"), {
                    title: _t('Alert!'),
                });
            }
            }
            else{

            }

        });

        // Click event For Deleting existing Academic Detail of Applicants
        $(document).on('click', '.delete_academic', function(e){
            var ele= $(this)
            e.stopPropagation();
            e.preventDefault();
            var id = parseInt($(this).data('academic_id'));
            odoo.jsonRpc("/delete_academic", 'call', {
              'id' : id,
            }).then(function (rec) {
                ele.closest('tr').remove()
//               location.reload();
            });
        });

        // Click event For Editing existing Academic Detail of Applicants
        $(document).on('click', '.edit_academic', function(e){

            e.stopPropagation();
            e.preventDefault();
            var id = $(this).data('academic_id');
            $('#myModalAcademic').modal();
            $('#myModalAcademic').find("h4[class='modal-title']").text("Update Academic Details")
            var target = $(this).parents('#AcademicEditModal'+id);

            $('#myModalAcademic').find("input[name='qualification']").val($.trim($(this).closest("tr").find('td:eq(0)').text()))
            $('#myModalAcademic').find("input[name='study_field']").val($.trim($(this).closest("tr").find('td:eq(1)').text()))
            $('#myModalAcademic').find("input[name='organization']").val($.trim($(this).closest("tr").find('td:eq(2)').text()))
            $('#myModalAcademic').find("input[name='location']").val($.trim($(this).closest("tr").find('td:eq(3)').text()))
            $('#myModalAcademic').find("input[name='start_date']").val($(this).closest("tr").find('td:eq(4) span').attr('data-oe-original'))
            $('#myModalAcademic').find("input[name='end_date']").val($(this).closest("tr").find('td:eq(5) span').attr('data-oe-original'))
            $('#myModalAcademic').find("input[name='grade']").val($.trim($(this).closest("tr").find('td:eq(6)').text()))
            $('#myModalAcademic').find("input[name='operation_type']").val('update')
            $('#myModalAcademic').find("input[name='opr_id']").val(id)
            $('#myModalAcademic').find("input[name='tr_no']").val($.trim($(this).closest("tr").index()))

            if($(this).closest("tr").find('td:eq(5) span').attr('data-oe-original')){

              $('#myModalAcademic').find("input[name='is_still']").prop("checked", false);
                 $('#myModalAcademic').find('.end_date_div').show();
            }
            else
            {
               $('#myModalAcademic').find("input[name='is_still']").prop("checked", true);
               $('#myModalAcademic').find('.end_date_div').hide();
            }


//            $('#myModalAcademic').find('')
//
//             odoo.jsonRpc("/edit_academic_applicant", 'call', {
//                    'qualification' : target.find("input[name='qualification']").val(),
//                    'study_field' : target.find("input[name='study_field']").val(),
//                    'organization' : target.find("input[name='organization']").val(),
//                    'location' : target.find("input[name='location']").val(),
//                    'start_date' : target.find("input[name='start_date']").val(),
//                    'end_date' : target.find("input[name='end_date']").val(),
//                    'grade' : target.find("input[name='grade']").val(),
//                    'id' : id
//                }).then(function() {
//                    location.reload();
//                });
//
        });

        // Click event For Editing existing exeperience Detail of Applicants
        // Validation on the models can/should be improved later on
        $(document).on('click', '#add_experience', function(e){
            e.stopPropagation();
            e.preventDefault();

            var current_val=new Date()
            var target = $(this).parents('#myModalExperience');
            if(target.find("input[name='operation_type']").val()=='update'){
                var start_date_val=new Date(target.find("input[name='start_date']").val())
                var end_date_val=new Date(target.find("input[name='end_date']").val())

                if(start_date_val>end_date_val){
                    alert("start date should not be greater than end date.")
                    return false
                }
                 if((start_date_val>=current_val)){
                    alert("start date  should not greater than or equal to today")
                    return false
                } if((end_date_val>=current_val)){
                    alert("end date should not greater than or equal to today")
                    return false
                }
                if ( $.trim(target.find("input[name='job_position']").val()) &&
                $.trim(target.find("input[name='organization']").val()) &&
                $.trim(target.find("input[name='location']").val()) &&
                $.trim(target.find("input[name='start_date']").val()) &&
                $.trim(target.find("input[name='contact_referee']").val()) &&
                $.trim(target.find("input[name='description']").val()) &&
                $.trim(target.find("input[name='position_referee']").val()) &&
                $.trim(target.find("input[name='name_referee']").val())
                ){
if($('#myModalExperience').find("input[name='is_still']").is(":checked")){
  var job_position = target.find("input[name='job_position']").val()
                     var organization = target.find("input[name='organization']").val()
                     var location =  target.find("input[name='location']").val()
                     var start_date = target.find("input[name='start_date']").val()
                     var is_still = true
                     var contact_referee = target.find("input[name='contact_referee']").val()
                     var description = target.find("input[name='description']").val()
                     var position_referee = target.find("input[name='position_referee']").val()
                     var name_referee = target.find("input[name='name_referee']").val()
                     var notice_period = target.find("select.notice_period").val()
                     var type = target.find("select.type").val()
                     var tr_no=parseInt(target.find("input[name='tr_no']").val())+1

//                     alert(tr_no,$('.exp_desc_table tr').length)

                     if ($('.exp_desc_table tr').length==2){
                        tr_no=1
                     }
                    odoo.jsonRpc("/edit_experience_applicant", 'call', {
                        'job_position' : target.find("input[name='job_position']").val(),
                        'organization' : target.find("input[name='organization']").val(),
                        'location' : target.find("input[name='location']").val(),
                        'start_date' : target.find("input[name='start_date']").val(),
                        'is_still':true,
                        'contact_referee' : target.find("input[name='contact_referee']").val(),
                        'description' : target.find("input[name='description']").val(),
                        'position_referee' : target.find("input[name='position_referee']").val(),
                        'name_referee' : target.find("input[name='name_referee']").val(),
                        'notice_period' : target.find("select.notice_period").val(),
                        'type' : target.find("select.type").val(),
                        'id' : target.find("input[name='opr_id']").val()
                    }).then(function(rec) {


                    if(target.find("input[name='contact_referee']").val()==''){
                 target.find("input[name='contact_referee']").css({'border':'1px solid red'})
                 alert("Please enter reference contact")
                 return false

            }
              else if(target.find("input[name='contact_referee']").val().match('^\d+$/')){
                   target.find("input[name='contact_referee']").css({'border':'1px solid red'})
                 alert("Please enter reference properly")
                 return false
                }
                     else if($('.mobile-applicant').val()<0){
             target.find("input[name='contact_referee']").css({'border':'1px solid red'})
                 alert("Please enter reference properly")
                 return false
         }

                         $(".exp_desc_table tr:eq("+$.trim(tr_no)+")").replaceWith("<tr><td>"+$.trim(job_position)+"</td><td>"+$.trim(start_date)+"</td><td>"+$.trim(end_date)+"</td><td>"+$.trim(organization)+"</td><td>"+$.trim(location)+"</td><td>"+$.trim(description)+"</td><td>"+$.trim(notice_period)+"</td><td>"+$.trim(name_referee)+"</td><td>"+$.trim(position_referee)+"</td><td>"+$.trim(contact_referee)+"</td><td>"+$.trim(type)+"</td><td><button type='button' class='btn edit_experience' data-toggle='modal' data-experience_id="+rec+"><i class='fa fa-pencil-square-o'></i></button><td><button type='button' data-experience_id="+rec+" class='btn delete_experience'><i class='fa fa-trash'></i></button></td></tr>")
                        $('#myModalExperience').modal('hide')
                        $( "#exp_desc_table" ).load(window.location.href + " #exp_desc_table" );
                    });}
                    else{
                     var job_position = target.find("input[name='job_position']").val()
                     var organization = target.find("input[name='organization']").val()
                     var location =  target.find("input[name='location']").val()
                     var start_date = target.find("input[name='start_date']").val()
                     var end_date = target.find("input[name='end_date']")
                     .val()
                     var contact_referee = target.find("input[name='contact_referee']").val()
                     var description = target.find("input[name='description']").val()
                     var position_referee = target.find("input[name='position_referee']").val()
                     var name_referee = target.find("input[name='name_referee']").val()
                     var notice_period = target.find("select.notice_period").val()
                     var type = target.find("select.type").val()
//                     var tr_no=target.find("input[name='tr_no']").val()
                    var tr_no=parseInt(target.find("input[name='tr_no']").val())+1
                     if ($('.exp_desc_table tr').length==2){
                        tr_no=1
                     }
                    odoo.jsonRpc("/edit_experience_applicant", 'call', {
                        'job_position' : target.find("input[name='job_position']").val(),
                        'organization' : target.find("input[name='organization']").val(),
                        'location' : target.find("input[name='location']").val(),
                        'start_date' : target.find("input[name='start_date']").val(),
                        'end_date' : target.find("input[name='end_date']").val(),
                        'contact_referee' : target.find("input[name='contact_referee']").val(),
                        'description' : target.find("input[name='description']").val(),
                        'position_referee' : target.find("input[name='position_referee']").val(),
                        'name_referee' : target.find("input[name='name_referee']").val(),
                        'notice_period' : target.find("select.notice_period").val(),
                        'type' : target.find("select.type").val(),
                        'id' : target.find("input[name='opr_id']").val()
                    }).then(function(rec) {


                    if(target.find("input[name='contact_referee']").val()==''){
                 target.find("input[name='contact_referee']").css({'border':'1px solid red'})
                 alert("Please enter reference contact")
                 return false

            }
              else if(target.find("input[name='contact_referee']").val().match('^\d+$/')){
                   target.find("input[name='contact_referee']").css({'border':'1px solid red'})
                 alert("Please enter reference properly")
                 return false
                }
                     else if($('.mobile-applicant').val()<0){
             target.find("input[name='contact_referee']").css({'border':'1px solid red'})
                 alert("Please enter reference properly")
                 return false
         }
   $(".exp_desc_table tr:eq("+$.trim(tr_no)+")").replaceWith("<tr><td>"+$.trim(job_position)+"</td><td>"+$.trim(start_date)+"</td><td>"+$.trim(end_date)+"</td><td>"+$.trim(organization)+"</td><td>"+$.trim(location)+"</td><td>"+$.trim(description)+"</td><td>"+$.trim(notice_period)+"</td><td>"+$.trim(name_referee)+"</td><td>"+$.trim(position_referee)+"</td><td>"+$.trim(contact_referee)+"</td><td>"+$.trim(type)+"</td><td><button type='button' class='btn edit_experience' data-toggle='modal' data-experience_id="+rec+"><i class='fa fa-pencil-square-o'></i></button><td><button type='button' data-experience_id="+rec+" class='btn delete_experience'><i class='fa fa-trash'></i></button></td></tr>")

                        $('#myModalExperience').modal('hide')
$( "#exp_desc_table" ).load(window.location.href + " #exp_desc_table" );
                    });

                    }
                } else {

                    Dialog.alert(self, _t("Please Give Proper Values to the Input fields !"), {
                        title: _t('Alert!'),
                    });
                }
            }
            else{
                var start_date_val=new Date(target.find("input[name='start_date']").val())
                var end_date_val=new Date(target.find("input[name='end_date']").val())

                if(start_date_val>end_date_val){
                    alert("Start date should not be greater than end date.")
                    return false
                }
                if((start_date_val>=current_val)){
                    alert("Start date  should not greater than or equal to today")
                    return false
                } if((end_date_val>=current_val)){
                    alert("End date should not greater than or equal to today")
                    return false
                }


                 if ( $.trim(target.find("input[name='job_position']").val()) &&
                $.trim(target.find("input[name='organization']").val()) &&
                $.trim(target.find("input[name='location']").val()) &&
                $.trim(target.find("input[name='start_date']").val()) &&
                $.trim(target.find("input[name='contact_referee']").val()) &&
                $.trim(target.find("input[name='description']").val()) &&
                $.trim(target.find("input[name='position_referee']").val()) &&
                $.trim(target.find("input[name='name_referee']").val()) &&
                $.trim(target.find("select.notice_period").val()) &&
                $.trim(target.find("select.type").val())
                ){
                 if($('#myModalExperience').find("input[name='is_still']").is(":checked")){
                     var job_position = target.find("input[name='job_position']").val()
                     var organization = target.find("input[name='organization']").val()
                     var location =  target.find("input[name='location']").val()
                     var start_date = target.find("input[name='start_date']").val()
                     var is_still = true
                     var contact_referee = target.find("input[name='contact_referee']").val()
                     var description = target.find("input[name='description']").val()
                     var position_referee = target.find("input[name='position_referee']").val()
                     var name_referee = target.find("input[name='name_referee']").val()
                     var notice_period = target.find("select.notice_period").val()
                     var type = target.find("select.type").val()
                    odoo.jsonRpc("/add_experience", 'call', {
                        'job_position' : target.find("input[name='job_position']").val(),
                        'organization' : target.find("input[name='organization']").val(),
                        'location' : target.find("input[name='location']").val(),
                        'start_date' : target.find("input[name='start_date']").val(),
                        'is_still' : true,
                        'contact_referee' : target.find("input[name='contact_referee']").val(),
                        'description' : target.find("input[name='description']").val(),
                        'position_referee' : target.find("input[name='position_referee']").val(),
                        'name_referee' : target.find("input[name='name_referee']").val(),
                        'notice_period' : target.find("select.notice_period").val(),
                        'type' : target.find("select.type").val(),
                    }).then(function(rec) {
                          if(target.find("input[name='contact_referee']").val()==''){
                 target.find("input[name='contact_referee']").css({'border':'1px solid red'})
                 alert("Please enter reference contact")
                 return false

            }
              else if(target.find("input[name='contact_referee']").val().match('^\d+$/')){
                   target.find("input[name='contact_referee']").css({'border':'1px solid red'})
                 alert("Please enter reference properly")
                 return false
                }
                     else if($('.mobile-applicant').val()<0){
             target.find("input[name='contact_referee']").css({'border':'1px solid red'})
                 alert("Please enter reference properly")
                 return false
         }

                        $('.exp_desc_table tr:last').after("<tr><td>"+$.trim(job_position)+"</td><td>"+$.trim(start_date)+"</td><td>"+$.trim(end_date)+"</td><td>"+$.trim(organization)+"</td><td>"+$.trim(location)+"</td><td>"+$.trim(description)+"</td><td>"+$.trim(notice_period)+"</td><td>"+$.trim(name_referee)+"</td><td>"+$.trim(position_referee)+"</td><td>"+$.trim(contact_referee)+"</td><td>"+$.trim(type)+"</td><td><button type='button' class='btn edit_experience' data-toggle='modal' data-experience_id="+rec+"><i class='fa fa-pencil-square-o'></i></button><td><button type='button' data-experience_id="+rec+" class='btn delete_experience'><i class='fa fa-trash'></i></button></td></tr>")
                        $('#myModalExperience').modal('hide')
//                        location.reload();
$( "#exp_desc_table" ).load(window.location.href + " #exp_desc_table" );
                    });}
                    else{
                     var job_position = target.find("input[name='job_position']").val()
                     var organization = target.find("input[name='organization']").val()
                     var location =  target.find("input[name='location']").val()
                     var start_date = target.find("input[name='start_date']").val()
                     var end_date = target.find("input[name='end_date']").val()
                     var contact_referee = target.find("input[name='contact_referee']").val()
                     var description = target.find("input[name='description']").val()
                     var position_referee = target.find("input[name='position_referee']").val()
                     var name_referee = target.find("input[name='name_referee']").val()
                     var notice_period = target.find("select.notice_period").val()
                     var type = target.find("select.type").val()
                     odoo.jsonRpc("/add_experience", 'call', {
                        'job_position' : target.find("input[name='job_position']").val(),
                        'organization' : target.find("input[name='organization']").val(),
                        'location' : target.find("input[name='location']").val(),
                        'start_date' : target.find("input[name='start_date']").val(),
                        'end_date' : target.find("input[name='end_date']").val(),
                        'contact_referee' : target.find("input[name='contact_referee']").val(),
                        'description' : target.find("input[name='description']").val(),
                        'position_referee' : target.find("input[name='position_referee']").val(),
                        'name_referee' : target.find("input[name='name_referee']").val(),
                        'notice_period' : target.find("select.notice_period").val(),
                        'type' : target.find("select.type").val(),
                    }).then(function(rec) {
                          if(target.find("input[name='contact_referee']").val()==''){
                 target.find("input[name='contact_referee']").css({'border':'1px solid red'})
                 alert("Please enter reference contact")
                 return false

            }
              else if(target.find("input[name='contact_referee']").val().match('^\d+$/')){
                   target.find("input[name='contact_referee']").css({'border':'1px solid red'})
                 alert("Please enter reference properly")
                 return false
                }
                     else if($('.mobile-applicant').val()<0){
             target.find("input[name='contact_referee']").css({'border':'1px solid red'})
                 alert("Please enter reference properly")
                 return false
                }

                        $('.exp_desc_table tr:last').after("<tr><td>"+$.trim(job_position)+"</td><td>"+$.trim(start_date)+"</td><td>"+$.trim(end_date)+"</td><td>"+$.trim(organization)+"</td><td>"+$.trim(location)+"</td><td>"+$.trim(description)+"</td><td>"+$.trim(notice_period)+"</td><td>"+$.trim(name_referee)+"</td><td>"+$.trim(position_referee)+"</td><td>"+$.trim(contact_referee)+"</td><td>"+$.trim(type)+"</td><td><button type='button' class='btn edit_experience' data-toggle='modal' data-experience_id="+rec+"><i class='fa fa-pencil-square-o'></i></button><td><button type='button' data-experience_id="+rec+" class='btn delete_experience'><i class='fa fa-trash'></i></button></td></tr>")
                        $('#myModalExperience').modal('hide')
$( "#exp_desc_table" ).load(window.location.href + " #exp_desc_table" );
                    });
                    }
                } else {
                    Dialog.alert(self, _t("Please Give Proper Values to the Input fields !"), {
                        title: _t('Alert!'),
                    });
                }
                }
        });

        // Click event For Deleting existing exeperience Detail of Applicants
        $(document).on('click', '.delete_experience', function(e){
            e.stopPropagation();
            e.preventDefault();
              var ele= $(this)
            var id = parseInt($(this).data('experience_id'));
            odoo.jsonRpc("/delete_experience", 'call', {
              'id' : id,
            }).then(function () {
                  ele.closest('tr').remove()

            });

        });

        // Click event For Editing existing exeperience Detail of Applicants
        $(document).on('click', '.edit_experience', function(e){
            e.stopPropagation();
            e.preventDefault();
            $('#myModalExperience').modal();
            var id = $(this).data('experience_id');

            var target = $(this).parents('#ExperienceEditModal'+id);
            $('#myModalExperience').find("h4[class='modal-title']").text("Update Experience Details")
            $('#myModalExperience').find("input[name='job_position']").val($.trim($(this).closest("tr").find('td:eq(0)').text()))
            $('#myModalExperience').find("input[name='start_date']").val($.trim($(this).closest("tr").find('td:eq(1) span').attr('data-oe-original')))
            $('#myModalExperience').find("input[name='end_date']").val($.trim($(this).closest("tr").find('td:eq(2) span').attr('data-oe-original')))
            $('#myModalExperience').find("input[name='organization']").val($.trim($(this).closest("tr").find('td:eq(3)').text()))
            $('#myModalExperience').find("input[name='location']").val($.trim($(this).closest("tr").find('td:eq(4)').text()))
            $('#myModalExperience').find("input[name='description']").val($.trim($(this).closest("tr").find('td:eq(5)').text()))
            $('#myModalExperience').find("input[name='name_referee']").val($.trim($(this).closest("tr").find('td:eq(7)').text()))
            $('#myModalExperience').find("input[name='position_referee']").val($.trim($(this).closest("tr").find('td:eq(8)').text()))
            $('#myModalExperience').find("input[name='contact_referee']").val($.trim($(this).closest("tr").find('td:eq(9)').text()))
            $('#myModalExperience').find("input[name='select.type']").val($.trim($(this).closest("tr").find('td:eq(10)').text()))
            $('#myModalExperience').find("input[name='operation_type']").val('update')
            $('#myModalExperience').find("input[name='opr_id']").val(id)
            $('#myModalExperience').find("input[name='tr_no']").val($.trim($(this).closest("tr").index()))
              if($(this).closest("tr").find('td:eq(2) span').attr('data-oe-original')){

              $('#myModalExperience').find("input[name='is_still']").prop("checked", false);
                 $('#myModalExperience').find('.end_date_div').show();
            }
            else
            {
               $('#myModalExperience').find("input[name='is_still']").prop("checked", true);
               $('#myModalExperience').find('.end_date_div').hide();
            }


        });


        $(document).on('click', '#add_certification', function(e){
            e.stopPropagation();
            e.preventDefault();
            var target = $(this).parents('#myModalCertification');
            var id=target.find("input[name='opr_id']").val()
             var current_val=new Date()
            var start_date_val=new Date(target.find("input[name='start_date']").val())
            var end_date_val=new Date(target.find("input[name='end_date']").val())
            if($('#myModalCertification').find("input[name='operation_type']").val()=='update'){
 if(start_date_val>end_date_val){
                    alert("Start date should not be greater than end date.")
                    return false
                }
                 if((start_date_val>=current_val)){
                    alert("Start date  should not greater than or equal to today")
                    return false
                } if((end_date_val>=current_val)){
                    alert("End date should not greater than or equal to today")
                    return false
                }

                if(target.find("input[name='start_date']").val()==''){
                alert("Please enter start date")
                return false
                }

                if($('#myModalCertification').find("input[name='is_still']").is(":checked")){
                 var name = target.find("input[name='name']").val()
                var certification = target.find("input[name='certification']").val()
                var organization = target.find("input[name='organization']").val()
                var location = target.find("input[name='location']").val()
                var start_date = target.find("input[name='start_date']").val()
                var is_still =  true
                var end_date=target.find("input[name='end_date']").val()
                var grade = target.find("input[name='grade']").val()
                var opr_id = target.find("input[name='opr_id']").val()
                 var tr_no=parseInt(target.find("input[name='tr_no']").val())+1
                     if ($('.certificate_desc_table tr').length==2){
                        tr_no=1
                     }
                   var description = target.find("input[name='description']").val()
                 odoo.jsonRpc("/edit_certification_applicant", 'call', {
                        'name' : target.find("input[name='name']").val(),
                        'organization' : target.find("input[name='organization']").val(),
                        'certification' : target.find("input[name='certification']").val(),
                        'location' : target.find("input[name='location']").val(),
                        'start_date' : target.find("input[name='start_date']").val(),
                        'grade' : target.find("input[name='grade']").val(),
                        'is_still' : true,
                        'description' : target.find("input[name='description']").val(),
                        'id' : id
                    }).then(function(rec) {
                       $(".certificate_desc_table tr:eq("+$.trim(tr_no)+")").replaceWith("<tr><td>"+$.trim(name)+"</td><td>"+$.trim(start_date)+"</td><td>"+$.trim(end_date)+"</td><td>"+$.trim(grade)+"</td><td>"+$.trim(organization)+"</td><td>"+$.trim(certification)+"</td><td>"+$.trim(location)+"</td><td>"+$.trim(description)+"</td><td><button type='button' class='btn edit_certificate' data-toggle='modal' data-certification_id="+rec+"><i class='fa fa-pencil-square-o'></i></button><td><button type='button' data-certification_id="+rec+" class='btn delete_certificate'><i class='fa fa-trash'></i></button></td></tr>")
                     $('#myModalCertification').modal('hide')
                     $( "#certificate_desc_table" ).load(window.location.href + " #certificate_desc_table" );
                    });
            }
            else{
             var name = target.find("input[name='name']").val()
                var certification = target.find("input[name='certification']").val()
                var organization = target.find("input[name='organization']").val()
                var location = target.find("input[name='location']").val()
                var start_date = target.find("input[name='start_date']").val()
                var is_still =  true
                var end_date=target.find("input[name='end_date']").val()
                var grade = target.find("input[name='grade']").val()
                var opr_id = target.find("input[name='opr_id']").val()
                var tr_no=parseInt(target.find("input[name='tr_no']").val())+1
                     if ($('.certificate_desc_table tr').length==2){
                        tr_no=1
                     }
if(target.find("input[name='start_date']").val()==''){
                alert("Please enter start date")
                return false
                }
                 var description = target.find("input[name='description']").val()
            odoo.jsonRpc("/edit_certification_applicant", 'call', {
                        'name' : target.find("input[name='name']").val(),
                        'organization' : target.find("input[name='organization']").val(),
                        'certification' : target.find("input[name='certification']").val(),
                        'location' : target.find("input[name='location']").val(),
                        'start_date' : target.find("input[name='start_date']").val(),
                        'grade' : target.find("input[name='grade']").val(),
                        'end_date' : target.find("input[name='end_date']").val(),
                        'description' : target.find("input[name='description']").val(),
                        'id' : id
                    }).then(function(rec) {
                       $(".certificate_desc_table tr:eq("+$.trim(tr_no)+")").replaceWith("<tr><td>"+$.trim(name)+"</td><td>"+$.trim(start_date)+"</td><td>"+$.trim(end_date)+"</td><td>"+$.trim(grade)+"</td><td>"+$.trim(organization)+"</td><td>"+$.trim(certification)+"</td><td>"+$.trim(location)+"</td><td>"+$.trim(description)+"</td><td><button type='button' class='btn edit_certificate' data-toggle='modal' data-certification_id="+rec+"><i class='fa fa-pencil-square-o'></i></button><td><button type='button' data-certification_id="+rec+" class='btn delete_certificate'><i class='fa fa-trash'></i></button></td></tr>")
                     $('#myModalCertification').modal('hide')
                     $( "#certificate_desc_table" ).load(window.location.href + " #certificate_desc_table" );
                    });
            }
            }
            else{
             if(start_date_val>end_date_val){
                    alert("Start date should not be greater than end date.")
                    return false
                }
                 if((start_date_val>=current_val)){
                    alert("Start date  should not greater than or equal to today")
                    return false
                } if((end_date_val>=current_val)){
                    alert("End date should not greater than or equal to today")
                    return false
                }
                  if ( $.trim(target.find("input[name='name']").val()) &&
                $.trim(target.find("input[name='organization']").val()) &&
                $.trim(target.find("input[name='certification']").val()) &&
                $.trim(target.find("input[name='location']").val()) &&
                $.trim(target.find("input[name='start_date']").val()) &&
                $.trim(target.find("input[name='description']").val())){

 if($('#myModalCertification').find("input[name='is_still']").is(":checked")){
 var name = target.find("input[name='name']").val()
                var certification = target.find("input[name='certification']").val()
                var organization = target.find("input[name='organization']").val()
                var location = target.find("input[name='location']").val()
                var start_date = target.find("input[name='start_date']").val()
                var is_still =  true
                var end_date=target.find("input[name='end_date']").val()
                var grade = target.find("input[name='grade']").val()
                var opr_id = target.find("input[name='opr_id']").val()
                 var tr_no = target.find("input[name='tr_no']").val()
                   var description = target.find("input[name='description']").val()
  odoo.jsonRpc("/add_certification", 'call', {
                        'name' : target.find("input[name='name']").val(),
                        'organization' : target.find("input[name='organization']").val(),
                        'certification' : target.find("input[name='certification']").val(),
                        'location' : target.find("input[name='location']").val(),
                        'grade' : target.find("input[name='grade']").val(),
                        'start_date' : target.find("input[name='start_date']").val(),
                        'is_still' : true,
                        'description' : target.find("input[name='description']").val(),
                    }).then(function(rec) {
                         $('.certificate_desc_table tr:last').after("<tr><td>"+$.trim(name)+"</td><td>"+$.trim(start_date)+"</td><td>"+$.trim(end_date)+"</td><td>"+$.trim(grade)+"</td><td>"+$.trim(organization)+"</td><td>"+$.trim(certification)+"</td><td>"+$.trim(location)+"</td><td>"+$.trim(description)+"</td><td><button type='button' class='btn edit_certificate' data-toggle='modal' data-certification_id="+rec+"><i class='fa fa-pencil-square-o'></i></button><td><button type='button' data-certification_id="+rec+" class='btn delete_certificate'><i class='fa fa-trash'></i></button></td></tr>")
                    $('#myModalCertification').modal('hide')
                    $( "#certificate_desc_table" ).load(window.location.href + " #certificate_desc_table" );
                    });
 }else{
   var certification = target.find("input[name='certification']").val()
   var name = target.find("input[name='name']").val()
                var organization = target.find("input[name='organization']").val()
                var location = target.find("input[name='location']").val()
                var start_date = target.find("input[name='start_date']").val()
                var is_still =  true
                var end_date=target.find("input[name='end_date']").val()
                var grade = target.find("input[name='grade']").val()
                var opr_id = target.find("input[name='opr_id']").val()
                var tr_no=parseInt(target.find("input[name='tr_no']").val())+1
                     if ($('.certificate_desc_table tr').length==2){
                        tr_no=1
                     }
                   var description = target.find("input[name='description']").val()
  odoo.jsonRpc("/add_certification", 'call', {
                        'name' : target.find("input[name='name']").val(),
                        'organization' : target.find("input[name='organization']").val(),
                        'certification' : target.find("input[name='certification']").val(),
                        'location' : target.find("input[name='location']").val(),
                        'grade' : target.find("input[name='grade']").val(),
                        'start_date' : target.find("input[name='start_date']").val(),
                        'end_date' : target.find("input[name='end_date']").val(),
                        'description' : target.find("input[name='description']").val(),
                    }).then(function(rec) {
                       $('.certificate_desc_table tr:last').after("<tr><td>"+$.trim(name)+"</td><td>"+$.trim(start_date)+"</td><td>"+$.trim(end_date)+"</td><td>"+$.trim(grade)+"</td><td>"+$.trim(organization)+"</td><td>"+$.trim(certification)+"</td><td>"+$.trim(location)+"</td><td>"+$.trim(description)+"</td><td><button type='button' class='btn edit_certificate' data-toggle='modal' data-certification_id="+rec+"><i class='fa fa-pencil-square-o'></i></button><td><button type='button' data-certification_id="+rec+" class='btn delete_certificate'><i class='fa fa-trash'></i></button></td></tr>")
                    $('#myModalCertification').modal('hide')
                    $( "#certificate_desc_table" ).load(window.location.href + " #certificate_desc_table" );
                    });

 }

                } else {
                    Dialog.alert(self, _t("Please Give Proper Values to the Input fields !"), {
                        title: _t('Alert!'),
                    });
                }
            }


        });

        // Click event For Deleting Certifications of the Applicants if Needed
        $(document).on('click', '.delete_certificate', function(e){
            e.stopPropagation();
            e.preventDefault();
             var ele= $(this)
            var id = parseInt($(this).data('certification_id'));
            odoo.jsonRpc("/delete_certificate", 'call', {
              'id' : id,
            }).then(function () {
                ele.closest('tr').remove()
            });
        });

        // Click event For Editing Certifications of the Applicants if Needed
        $(document).on('click', '.edit_certificate', function(e){
            e.stopPropagation();
            e.preventDefault();
            $('#myModalCertification').modal();
            var id = $(this).data('certification_id');
            var target = $(this).parents('#CertificationEditModal'+id);
            $('#myModalCertification').find("h4[class='modal-title']").text("")
            $('#myModalCertification').find("h4[class='modal-title']").text("Update Certification Details")

              $('#myModalCertification').find("input[name='name']").val($.trim($(this).closest("tr").find('td:eq(0)').text()))
              $('#myModalCertification').find("input[name='start_date']").val($.trim($(this).closest("tr").find('td:eq(1) span').attr('data-oe-original')))
              $('#myModalCertification').find("input[name='end_date']").val($.trim($(this).closest("tr").find('td:eq(2) span').attr('data-oe-original')))
              $('#myModalCertification').find("input[name='grade']").val($.trim($(this).closest("tr").find('td:eq(3)').text()))
              $('#myModalCertification').find("input[name='organization']").val($.trim($(this).closest("tr").find('td:eq(4)').text()))
              $('#myModalCertification').find("input[name='certification']").val($.trim($(this).closest("tr").find('td:eq(5)').text()))
              $('#myModalCertification').find("input[name='location']").val($.trim($(this).closest("tr").find('td:eq(6)').text()))
              $('#myModalCertification').find("input[name='description']").val($.trim($(this).closest("tr").find('td:eq(7)').text()))
              $('#myModalCertification').find("input[name='operation_type']").val('update')
              $('#myModalCertification').find("input[name='opr_id']").val(id)
$('#myModalCertification').find("input[name='tr_no']").val($.trim($(this).closest("tr").index()))


                  if($(this).closest("tr").find('td:eq(2) span').attr('data-oe-original')){

              $('#myModalCertification').find("input[name='is_still']").prop("checked", false);
                 $('#myModalCertification').find('.end_date_div').show();
            }
            else
            {
               $('#myModalCertification').find("input[name='is_still']").prop("checked", true);
               $('#myModalCertification').find('.end_date_div').hide();
            }
        });

        // Click event For Adding Job Benefits  by Employers
        $(document).on('click', '#add_benefits', function(e){
            e.stopPropagation();
            e.preventDefault();
            if (!$("input[name='benefits']").val()){
                Dialog.alert(self, _t("Please add value in the Benefits input !"), {
                    title: _t('Alert!'),
                });
            } else {
//                $(this).hide();
                odoo.jsonRpc("/add_benefits", 'call', {
                    'job_id' : $("input[name='job_id']").val(),
                    'benefits' : $("input[name='benefits']").val(),
                }).then(function(result) {
                    if (result){
                    $("input[name='benefits']").val("")
                        Dialog.alert(self, _t("Job Benefits Has been successfully added for this job posting !"), {
                            confirm_callback: function() {
                            },
                            title: _t('Success!'),
                        });
                    } else {
                        Dialog.alert(self, _t("Job Benefits could not be added. Please try again !"), {
                            confirm_callback: function() {
                                location.reload();
                            },
                            title: _t('Alert'),
                        });
                    }
                });
            }
        });

        // Click event For Adding Job Requirements  by Employers
        $(document).on('click', '#add_job_requirements', function(e){
            e.stopPropagation();
            e.preventDefault();
            if (!$("input[name='job_requirements']").val()){
                Dialog.alert(self, _t("Please add value in the Job Requirements Input !"), {
                    title: _t('Alert!'),
                });
            } else {
//                $(this).hide();
                odoo.jsonRpc("/add_job_requirements", 'call', {
                    'job_id' : $("input[name='job_id']").val(),
                    'job_requirements' : $("input[name='job_requirements']").val(),
                }).then(function(result) {
                    if (result){
                    $("input[name='job_requirements']").val("")
                        Dialog.alert(self, _t("Job Requirement Has been successfully added for this job posting !"), {
                            confirm_callback: function() {

                            },
                            title: _t('Success!'),
                        });
                    } else {
                        Dialog.alert(self, _t("Job Requirement could not be added. Please try again !"), {
                            confirm_callback: function() {
                                location.reload();
                            },
                            title: _t('Alert'),
                        });
                    }
                });
            }
        });

        // Click event For Adding Job Location  by Employers
        $(document).on('click', '#add_job_location', function(e){
            e.stopPropagation();
            e.preventDefault();
            if (!$("input[name='job_location']").val()){
                Dialog.alert(self, _t("Please add value in the Job Location Input !"), {
                    title: _t('Alert!'),
                });
            } else {
//                $(this).hide();
                odoo.jsonRpc("/add_job_location", 'call', {
                    'job_id' : $("input[name='job_id']").val(),
                    'job_location' : $("input[name='job_location']").val(),
                }).then(function(result) {
                    if (result){
                    $("input[name='job_location']").val("")
                        Dialog.alert(self, _t("Job Location Has been successfully added for this job posting !"), {
                            confirm_callback: function() {
//                                location.reload();
                            },
                            title: _t('Success!'),
                        });
                    } else {
                        Dialog.alert(self, _t("Job Location could not be added. Please try again !"), {
                            confirm_callback: function() {
                                location.reload();
                            },
                            title: _t('Alert'),
                        });
                    }
                });
            }
        });

        // For Industry Practices Static Page JS
        $("div.bhoechie-tab-menu>div.list-group>a").click(function(e) {
            e.stopPropagation();
            e.preventDefault();
            $(this).siblings('a.active').removeClass("active");
            $(this).addClass("active");
            var index = $(this).index();
            $("div.bhoechie-tab>div.bhoechie-tab-content").removeClass("active");
            $("div.bhoechie-tab>div.bhoechie-tab-content").eq(index).addClass("active");
        });
    });
});
