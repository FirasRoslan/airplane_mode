# tasks.py
import frappe
from frappe.utils import getdate, add_days

def send_rent_reminders():
    """
    Simple reminder: send email for Rent Payments with payment_status 'Unpaid'
    whose period_end is within reminder window (e.g. today + X days).
    """
    try:
        settings = None
        try:
            settings = frappe.get_single("Shop Settings")
            reminder_days = int(settings.reminder_days_before_due or 7)
        except Exception:
            reminder_days = 7

        target_date = add_days(getdate(), reminder_days)

        payments = frappe.get_all(
            "Rent Payment",
            filters={"payment_status": "Unpaid", "period_end": target_date},
            fields=["name", "tenant", "shop", "amount", "period_end"]
        )

        for p in payments:
            tenant_email = frappe.db.get_value("Tenant", p.tenant, "email")
            if tenant_email:
                frappe.sendmail(
                    recipients=[tenant_email],
                    subject="Rent due reminder",
                    message=f"Dear Tenant,\n\nYour rent for shop {p.shop} (amount: {p.amount}) is due on {p.period_end}.\n\nRegards."
                )
    except Exception as e:
        frappe.log_error(message=str(e), title="send_rent_reminders error")
