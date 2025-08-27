frappe.ui.form.on("Airplane Ticket", {
    refresh: function(frm) {
        frm.add_custom_button("Assign Seat", function() {
            frappe.prompt([
                {
                    label: "Seat Number",
                    fieldname: "seat",
                    fieldtype: "Data",
                    reqd: 1
                }
            ],
            function(values){
                frm.set_value("seat", values.seat);
                frm.save();
                frappe.msgprint("Seat assigned: " + values.seat);
            },
            "Assign Seat",
            "Assign");
        });
    }
});
