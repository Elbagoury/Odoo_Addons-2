odoo.define('website_order_delivery_duration_drc', function (require){
    
    var core = require('web.core');
    var _t = core._t;

    $(document).ready(function(){
        var current_date = new Date()
        $("#delivery_date").datepicker({minDate: current_date})
        $("#delivery_date").on('change',function(){
            $('#message').remove()
            var input_date = new Date($("#delivery_date").val());
            var current_date = new Date();
            if(current_date > input_date){    
                var current_date = current_date.toJSON().slice(0,10).replace(/-/g,'/').split("/");
                var set_date = current_date[1] + "/" + current_date[2] + "/" + current_date[0];
                $("#delivery_date").val(set_date);
                $("#delivery_date").before('<h5 id="message" class="bg-danger text-center" style="padding: 15px;"><strong>'+_t("Can\'t allow to add past date.")+'</strong></h5>');
            }
        })
    })
});

