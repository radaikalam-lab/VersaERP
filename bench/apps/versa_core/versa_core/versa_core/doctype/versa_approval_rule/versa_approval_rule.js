frappe.ui.form.on('Versa Approval Rule', {
    refresh: function(frm) {
        frm.set_query('business_unit', function() {
            return {
                filters: {
                    'is_group': 0
                }
            };
        });
    }
});
