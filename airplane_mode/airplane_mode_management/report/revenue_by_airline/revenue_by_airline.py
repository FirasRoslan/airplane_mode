import frappe

def execute(filters=None):
    # 1) ambil semua airlines
    airlines = frappe.get_all("Airline", fields=["name"], order_by="name asc")

    data = []
    total_revenue = 0.0

    for a in airlines:
        airline_name = a.name

        # 2) dapatkan airplanes untuk airline ni
        airplanes = frappe.get_all("Airplane", filters={"airline": airline_name}, pluck="name")
        if not airplanes:
            # tiada airplane -> revenue 0
            revenue = 0.0
        else:
            # 3) dapatkan flights untuk airplane yang tersenarai
            flights = frappe.get_all("Airplane Flight", filters={"airplane": ["in", airplanes]}, pluck="name")

            if not flights:
                revenue = 0.0
            else:
                # 4) jumlahkan total_amount dari Airplane Ticket yang flight in flights
                # gunakan frappe.db.get_value dengan aggregation
                revenue = frappe.db.get_value(
                    "Airplane Ticket",
                    filters={"flight": ["in", flights]},
                    fieldname="sum(total_amount)"
                ) or 0.0

        # append ke data
        data.append({
            "airline": airline_name,
            "revenue": float(revenue) if revenue is not None else 0.0
        })
        total_revenue += float(revenue or 0.0)

    # columns
    columns = [
        {"label": "Airline", "fieldname": "airline", "fieldtype": "Link", "options": "Airline", "width": 250},
        {"label": "Revenue", "fieldname": "revenue", "fieldtype": "Currency", "width": 150},
    ]

    # summary (Total Revenue)
    summary = [
        {"label": "Total Revenue", "value": total_revenue, "datatype": "Currency"}
    ]

    # chart (donut)
    chart = {
        "data": {
            "labels": [row["airline"] for row in data],
            "datasets": [{"values": [row["revenue"] for row in data]}]
        },
        "type": "donut",
        "height": 300
    }

    # return columns, data, message, chart, summary
    return columns, data, None, chart, summary
