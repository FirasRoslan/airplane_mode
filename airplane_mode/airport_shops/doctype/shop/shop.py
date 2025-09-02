import frappe
from frappe.website.website_generator import WebsiteGenerator

class Shop(WebsiteGenerator):
    def validate(self):
        if self.get("status") == "Occupied":
            if not self.get("tenant"):
                frappe.throw("Tenant must be filled in when Shop changes to 'Occupied'.")
            if not self.get("contract_start") or not self.get("contract_end"):
                frappe.throw("Please fill in Contract Start and Contract End.")

    def before_insert(self):
        settings = frappe.get_single("Shop Settings")
        if not self.default_rent and settings.default_rent:
            self.default_rent = settings.default_rent
