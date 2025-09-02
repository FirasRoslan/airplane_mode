# rent_payment.py
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class RentPayment(Document):
    def before_save(self):
        # autofill tenant from shop
        if hasattr(self, "shop") and not getattr(self, "tenant", None):
            self.tenant = frappe.db.get_value("Shop", self.shop, "tenant")

        # default amount from shop.default_rent or Shop Settings
        if not getattr(self, "amount", None):
            amt = frappe.db.get_value("Shop", self.shop, "default_rent")
            if not amt:
                try:
                    settings = frappe.get_single("Shop Settings")
                    amt = getattr(settings, "default_rent_amount", None)
                except Exception:
                    amt = None
            self.amount = amt or 0.0

        # if status is Paid, set paid_on and receipt_no
        if getattr(self, "payment_status", None) == "Paid":
            if not getattr(self, "paid_on", None):
                self.paid_on = now_datetime()
            if not getattr(self, "receipt_no", None):
                import datetime, random
                dt = datetime.datetime.now().strftime("%Y%m%d")
                rnd = random.randint(1000,9999)
                self.receipt_no = f"RCPT-{dt}-{rnd}"

    def validate(self):
        # optional check: ensure tenant matches shop.tenant
        if getattr(self, "shop", None) and getattr(self, "tenant", None):
            tenant_from_shop = frappe.db.get_value("Shop", self.shop, "tenant")
            if tenant_from_shop and tenant_from_shop != self.tenant:
                frappe.throw("Tenant does not match shop's assigned tenant. Please check.")
