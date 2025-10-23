import frappe

def execute(filters=None):
    columns = [
        {"label": "Member ID", "fieldname": "name", "fieldtype": "Data", "width": 120},
        {"label": "Full Name", "fieldname": "full_name", "fieldtype": "Data", "width": 200},
        {"label": "Email", "fieldname": "email_address", "fieldtype": "Data", "width": 200},
        {"label": "Membership Start", "fieldname": "from_date", "fieldtype": "Date", "width": 120},
        {"label": "Membership Expiry", "fieldname": "to_date", "fieldtype": "Date", "width": 120},
    ]

    data = frappe.db.sql("""
        SELECT 
            lm.name,
            lm.full_name,
            lm.email_address,
            last_mem.from_date,
            last_mem.to_date
        FROM `tabLibrary Member` lm
        LEFT JOIN (
            SELECT 
                lms.library_member,
                lms.from_date,
                lms.to_date
            FROM `tabLibrary Membership` lms
            INNER JOIN (
                SELECT 
                    library_member, 
                    MAX(from_date) AS max_from_date
                FROM `tabLibrary Membership`
                GROUP BY library_member
            ) latest
            ON latest.library_member = lms.library_member 
            AND latest.max_from_date = lms.from_date
        ) AS last_mem ON lm.name = last_mem.library_member
        WHERE last_mem.to_date >= CURDATE()
        GROUP BY lm.name
        ORDER BY lm.full_name ASC
    """, as_dict=True)

    return columns, data
