# Copyright (c) 2025, Muhammad Firas and contributors
# For license information, please see license.txt

import frappe
import random
import string 
from frappe.model.document import Document


class AirplaneTicket(Document):
	def validate(self):
		add_ons_total = sum([d.amount for d in self.add_ons])
		self.total_amount = self.flight_price + add_ons_total 

		seen = set()
		unique_addons = []
		for d in self.add_ons:
			if d.item not in seen:
				seen.add(d.item)
				unique_addons.append(d)

		self.set("add_ons", unique_addons)

		# self.docstatus = 1, then self.status = "Booked"

	def before_submit(self):
		if self.status != "Boarded":
			frappe.throw("Ticket can only be submitted if status is 'Boarded'")


	def before_insert(self):
        # Generate seat automatically sebelum doc disave
		number = random.randint(1, 99)   # random nombor 1 - 99
		letter = random.choice(['A','B','C','D','E'])  # random huruf seat
		self.seat = f"{number}{letter}"