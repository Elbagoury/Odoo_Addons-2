odoo.define('multi_company_email.Session', function (require) {
    "use strict";

    var session = require('web.session');
    var SwitchCompanyMenu = require('web.SwitchCompanyMenu');

    SwitchCompanyMenu.include({
        _onSwitchCompanyClick: function (ev) {
            var dropdownItem = $(ev.currentTarget).parent();
            var companyID = dropdownItem.data('company-id');
            console.log('ESTOU AQUI :)' + session.uid);
            this._rpc({
                model: 'res.users',
                args: [session.uid, companyID],
                method: 'compute_user_signature',
            });
            this._super.apply(this, arguments);
        },
    });

});
