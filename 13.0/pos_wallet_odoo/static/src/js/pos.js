odoo.define('pos_wallet_odoo.pos', function(require) {
	"use strict";

	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var core = require('web.core');
	var gui = require('point_of_sale.gui');
	var popups = require('point_of_sale.popups');
	var rpc = require('web.rpc');

	var QWeb = core.qweb;
	var _t = core._t;
	var total_amt =0.0
	var entered_amount =0.0
	var my_user = 0;


	var _super_posmodel = models.PosModel.prototype;
	models.PosModel = models.PosModel.extend({
		initialize: function (session, attributes) {
			var partner_model = _.find(this.models, function(model){ return model.model === 'res.partner'; });
			partner_model.fields.push('wallet_balance');

			var payment_method = _.find(this.models, function(model){ return model.model === 'pos.payment.method'; });
			payment_method.fields.push('wallet');
						
			return _super_posmodel.initialize.call(this, session, attributes);
			
		},
		push_order: function(order, opts){
			var self = this;
			var pushed = _super_posmodel.push_order.call(this, order, opts);
			var client = order && order.get_client();
			
			if (client){
				order.paymentlines.each(function(line){
			
					var amount = line.get_amount();
					
					if (line.payment_method['wallet'] === true){
					if (amount <= client.wallet_balance){
					  var updated = client.wallet_balance - amount;
					  
						rpc.query({
							model: 'res.partner',
							method: 'write',
							args: [[client.id], {'wallet_balance': updated}],
						});
					
					}
					else{
					}
				   }
				});
			}
			return pushed;
		}
	});


	// ClientListScreenWidget start
	gui.Gui.prototype.screen_classes.filter(function(el) { return el.name == 'clientlist'})[0].widget.include({
		display_client_details: function(visibility,partner,clickpos){
			var self = this;
			var contents = this.$('.client-details-contents');
			var parent   = this.$('.client-list').parent();
			var scroll   = parent.scrollTop();
			var height   = contents.height();

			contents.off('click','.button.edit');
			contents.off('click','.button.save');
			contents.off('click','.button.undo');
			contents.on('click','.button.edit',function(){ self.edit_client_details(partner); });
			contents.on('click','.button.save',function(){ self.save_client_details(partner); });
			contents.on('click','.button.undo',function(){ self.undo_client_details(partner); });
			this.editing_client = false;
			this.uploaded_picture = null;

			if(visibility === 'show'){
				contents.empty();
				contents.append($(QWeb.render('ClientDetails',{widget:this,partner:partner})));

				var new_height   = contents.height();

				if(!this.details_visible){
					if(clickpos < scroll + new_height + 20 ){
						parent.scrollTop( clickpos - 20 );
					}else{
						parent.scrollTop(parent.scrollTop() + new_height);
					}
				}else{
					parent.scrollTop(parent.scrollTop() - height + new_height);
				}

				this.details_visible = true;
				
				// Click on Button, Open Popup pos-wallet Here...
				contents.on('click','.button.pos-wallet',function(){
					self.gui.show_popup('pos_wallet_popup_widget', { 'partner': partner });

				});
				// End Custom Code...
				
				
				this.toggle_save_button();
			} else if (visibility === 'edit') {
				this.editing_client = true;
				contents.empty();
				contents.append($(QWeb.render('ClientDetailsEdit',{widget:this,partner:partner})));
				this.toggle_save_button();

				contents.find('.image-uploader').on('change',function(){
					self.load_image_file(event.target.files[0],function(res){
						if (res) {
							contents.find('.client-picture img, .client-picture .fa').remove();
							contents.find('.client-picture').append("<img src='"+res+"'>");
							contents.find('.detail.picture').remove();
							self.uploaded_picture = res;
						}
					});
				});
			} else if (visibility === 'hide') {
				contents.empty();
				if( height > scroll ){
					contents.css({height:height+'px'});
					contents.animate({height:0},400,function(){
						contents.css({height:''});
					});
				}else{
					parent.scrollTop( parent.scrollTop() - height);
				}
				this.details_visible = false;
				this.toggle_save_button();
			}
		},
		close: function(){
			this._super();
		},
	});


	// PosWalletPopupWidget Popup start

	var PosWalletPopupWidget = popups.extend({
		template: 'PosWalletPopupWidget',
		init: function(parent, args) {
			this._super(parent, args);
			this.options = {};
		},
		events: {
			'click #add_wallet_money': 'do_wallet_recharge',
			'click .button.cancel': 'click_cancel',
		},

		//
		show: function(options) {
			this._super(options);
			this.partner = options.partner || [];
			this.renderElement();

		},
		//

		remove_current_orderlines: function(){
			var self = this;
			var order = this.pos.get_order();
			var orderlines = order.get_orderlines();
			if(orderlines.length > 0){
				for (var line in orderlines)
				{
					order.remove_orderline(order.get_orderlines());
				}
			} 
		},

		do_wallet_recharge: function(event, $el) {
			var self = this;
			var partner_id = this.partner;
			var entered_amount = $("#wallet_amount").val();
			var order = this.pos.get_order();
			if(!entered_amount || entered_amount <= 0){
				this.gui.show_popup('error',{
					'title': _t('Amount not defined.'),
					'body': _t('Please enter amount valid amount.'),
				});
				return;
			}
			else{
				self.remove_current_orderlines();
				var prd = self.pos.db.get_product_by_id(self.pos.config.wallet_recharge_product_id[0]);
				order.add_product(prd, {
					quantity: 1.0,
					price: parseFloat(entered_amount),
					discount: 0,
				});
				order.set_is_wallet_recharge(true);
				order.get_selected_orderline().set_wallet_recharge_line(true);
				order.set_client(partner_id);
				self.gui.show_screen('products');
			}
		},

		renderElement: function() {
			var self = this;
			this._super();
		},

	});
	gui.define_popup({
		name: 'pos_wallet_popup_widget',
		widget: PosWalletPopupWidget
	});

	// End Popup start


	var OrderSuper = models.Order;
	models.Order = models.Order.extend({
		init: function(parent,options){
			this._super(parent,options);
			this.is_wallet_recharge = this.is_wallet_recharge || false;
		},

		set_is_wallet_recharge: function(is_wallet_recharge){
			this.is_wallet_recharge = is_wallet_recharge;
			this.trigger('change',this);
		},

		get_is_wallet_recharge: function(is_wallet_recharge){
			return this.is_wallet_recharge;
		},
		
		export_as_JSON: function() {
			var self = this;
			var loaded = OrderSuper.prototype.export_as_JSON.call(this);
			loaded.is_wallet_recharge = self.is_wallet_recharge || false;
			return loaded;
		},

		init_from_JSON: function(json){
			OrderSuper.prototype.init_from_JSON.apply(this,arguments);
			this.is_wallet_recharge = json.is_wallet_recharge || false;
		},

		remove_orderline: function( line ){
			if(line.wallet_recharge_line){
				this.set_is_wallet_recharge(false);
			}
			this.assert_editable();
			this.orderlines.remove(line);
			this.select_orderline(this.get_last_orderline());
		},

		set_client: function(client){
			this.assert_editable();
			if(client)
			{
				if(total_amt>0)
				{
					if(my_user == client['id'])
					{
						client['wallet_balance'] = total_amt
					}
				}
			}
			
			this.set('client',client);
		},

	});

	var OrderlineSuper = models.Orderline.prototype;
	models.Orderline = models.Orderline.extend({
		initialize: function(attr,options){
		OrderlineSuper.initialize.apply(this, arguments);
			this.pos   = options.pos;
			this.wallet_recharge_line = this.wallet_recharge_line || false;
		},

		set_wallet_recharge_line: function(wallet_recharge_line){
			this.wallet_recharge_line = wallet_recharge_line;
			this.trigger('change',this);
		},

		get_wallet_recharge_line: function(wallet_recharge_line){
			return this.wallet_recharge_line;
		},
		
		export_as_JSON: function() {
			var self = this;
			var loaded = OrderlineSuper.export_as_JSON.call(this);
			loaded.wallet_recharge_line = self.wallet_recharge_line || false;
			return loaded;
		},

		init_from_JSON: function(json){
			OrderlineSuper.init_from_JSON.apply(this,arguments);
			this.wallet_recharge_line = json.wallet_recharge_line || false;
		},
	});

	screens.ProductListWidget.include({
		init: function(parent, options) {
			var self = this;
			this._super(parent,options);
			
			this.click_product_handler = function(){
				var order = self.pos.get_order();
				var orderlines = order.get_orderlines();

				var product = self.pos.db.get_product_by_id(this.dataset.productId);
				
				// Deny POS Order When Product is Out of Stock
				if(orderlines.length == 1 && orderlines[0]){
					if(orderlines[0].wallet_recharge_line){
						self.gui.show_popup('error',{
							'title': _t('Wallet Recharge Order.'),
							'body': _t('You can not add other product in Wallet Recharge Order.'),
						});
					}else{
						options.click_product_action(product);
					}
				}else {
					options.click_product_action(product);
				}
			};

		},
   
	});


	// PaymentScreenWidget start
	screens.PaymentScreenWidget.include({

		show: function(){
			var client = this.pos.get_client();
			// this.$('#payment_wallet').text( total_amt ? _t("[Wallet :"+total_amt+"]") : client.wallet_balance ); 
			if(client)
			{
				if(client['id'] == my_user)
				{
					if(total_amt>0)
					{
						this.$('#payment_wallet').text( client ? "[Wallet :"+total_amt+"]" : '' );  
					}
					else
					{
						this.$('#payment_wallet').text( client ? "[Wallet :"+client.wallet_balance+"]" : '' );
					}    
				}
				else
				{
					this.$('#payment_wallet').text( client ? "[Wallet :"+client.wallet_balance+"]" : '' );
				} 
			}
			
			this._super();
		},

		customer_changed: function() {
			var client = this.pos.get_client();
			this.$('.js_customer_name').text( client ? client.name : _t('Customer') );
			this.$('#payment_wallet').text( client ? "[Wallet :"+total_amt+"]" : "" );  
		},

		click_paymentmethods: function(id) {
			var payment_method = this.pos.payment_methods_by_id[id];
			var order = this.pos.get_order();
			if(order.is_wallet_recharge && payment_method.wallet){
				this.gui.show_popup('error',{
					'title': _t('Wrong Payment Method'),
					'body':  _t('You can not recharge wallet using wallet journal.'),
				});
			}
			else{
				this._super(id);
			}
		},

		validate_order: function(options) {
			var currentOrder = this.pos.get_order();
			
			var plines = currentOrder.get_paymentlines();
			
			var dued = currentOrder.get_due();
			
			var changed = currentOrder.get_change();
			
			var clients = currentOrder.get_client();
			
			if (clients){  //if customer is selected
				for (var i = 0; i < plines.length; i++) {
				   if (plines[i].payment_method['wallet'] === true) { //we've given cash Type
					   if(plines[i]['amount'] > clients.wallet_balance){ // Make Condition that amount is greater than selected customer's wallet amount
						   this.gui.show_popup('error',{
								'title': _t('Not Sufficient Wallet Balance'),
								'body': _t('Customer has not Sufficient Wallet Balance To Pay'),
							});
							return;
					}
				  }
				} 
			}
			
			for (var i = 0; i < plines.length; i++) {

				if (plines[i].payment_method['wallet'] === true){
				  
				   if(currentOrder.get_change() > 0){ // Make Condition that amount is greater than selected customer's wallet amount
					   this.gui.show_popup('error',{
						'title': _t('Payment Amount Exceeded'),
						'body': _t('You cannot Pay More than Total Amount'),
					});
					return;
					}
				
					// Make Condition: Popup Occurs When Customer is not selected on wallet payment method, While any other payment method, this error popup will not be showing
					if (!currentOrder.get_client()){
						this.gui.show_popup('error',{
							'title': _t('Unknown customer'),
							'body': _t('You cannot use Wallet payment. Select customer first.'),
						});
						return;
					}
				
				}
			} 

			if(currentOrder.get_orderlines().length === 0){
				this.gui.show_popup('error',{
					'title': _t('Empty Order'),
					'body': _t('There must be at least one product in your order before it can be validated.'),
				});
				return;
			}
			total_amt = 0.0
			this._super(options);
		},

	});
	
		
	

});
