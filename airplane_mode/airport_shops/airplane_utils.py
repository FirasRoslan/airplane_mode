# airplane_utils.py
import frappe
from frappe.utils import now_datetime
from frappe.utils.background_jobs import enqueue

def update_ticket_gate_handler(doc, method=None):
    """
    Called by hooks doc_events when Airplane Flight is updated.
    Enqueue the background job to update all tickets for that flight.
    """
    try:
        # enqueue the background job
        enqueue("airport_shops.airplane_utils._update_ticket_gate", flight=doc.name, gate=doc.get("gate_number"))
    except Exception as e:
        frappe.log_error(message=str(e), title="enqueue update_ticket_gate error")

@frappe.whitelist()
def _update_ticket_gate(flight, gate=None):
    try:
        tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight}, pluck="name")
        for t in tickets:
            # use db_set to avoid heavy triggers if you want fast update
            frappe.db.set_value("Airplane Ticket", t, "gate_number", gate)
    except Exception as e:
        frappe.log_error(message=str(e), title="_update_ticket_gate error")
