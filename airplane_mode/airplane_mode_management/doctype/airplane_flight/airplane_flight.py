# Copyright (c) 2025, Muhammad Firas and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class AirplaneFlight(WebsiteGenerator):
    def on_submit(self):
        self.status = "Completed"

    def on_update(self):
        # enqueue background job bila gate_number berubah
        frappe.enqueue(
            "airport_shops.tasks.update_tickets_gate",
            flight=self.name,
            gate=self.gate_number
        )

