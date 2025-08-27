frappe.ui.form.on("Airline", {
    refresh: function(frm) {
        // hanya tunjuk link kalau website ada value
        if (frm.doc.website) {
            frm.add_web_link(frm.doc.website, "Visit Airline Website");
        }
    }
});
