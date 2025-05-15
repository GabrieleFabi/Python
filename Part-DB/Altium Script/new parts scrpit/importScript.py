import csv
 
input_file = 'Altium.csv'
output_file = 'formatted_output.csv'
default_tag = "Inverter - Logica"
 
output_headers = [
    "name", "description", "category", "notes", "footprint", "tags", "quantity",
    "storage", "mass", "ipn", "mpn", "manufacturing_status", "manufacturer",
    "supplier", "spn", "price", "favourite", "needs_review", "minamount",
    "partUnit", "manufacturing_status"
]
 
# Keys we expect in the actual header row
expected_keys = {"mpn1", "description", "quantity", "designator", "mfg1"}
 
with open(input_file, newline='', encoding='cp1252') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
 
    # 🔍 Find the real header row
    for row in reader:
        normalized = [col.strip().lower() for col in row]
        if expected_keys & set(normalized):
            header = row
            break
    else:
        raise ValueError("Couldn't find a valid header row in the file.")
 
    # Map normalized names to actual header
    normalized_header_map = {
        h.strip().lower(): h for h in header
    }
 
    rows = []
    for row_values in reader:
        if all(not v.strip() for v in row_values):
            continue
 
        row_dict = dict(zip(header, row_values))
 
        def get_val(key):
            actual_key = normalized_header_map.get(key.lower())
            return row_dict.get(actual_key, "").strip() if actual_key else ""
 
        output_row = {
            "name": get_val("mpn1"),
            "description": get_val("description"),
            "category": "",
            "notes": get_val("designator"),
            "footprint": "",
            "tags": default_tag,
            "quantity": "",
            "storage": "",
            "mass": "",
            "ipn": "",
            "mpn": get_val("mpn1"),
            "manufacturing_status": "",
            "manufacturer": get_val("mfg1"),
            "supplier": "Mouser",
            "spn": "",
            "price": "",
            "favourite": "0",
            "needs_review": "0",
            "minamount": "",
            "partUnit": "",
            "manufacturing_status": ""
        }
 
        rows.append(output_row)
 
# ✅ Write the output CSV
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=output_headers, delimiter=';')
    writer.writeheader()
    writer.writerows(rows)