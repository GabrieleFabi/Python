import csv
from collections import defaultdict

input_file = 'Altium.csv'
output_file = 'output.csv'

with open(input_file, newline='', encoding='cp1252') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')

    # Normalize fieldnames
    fieldnames = [name.strip().lower() for name in reader.fieldnames]

    field_map = {}
    for name in fieldnames:
        lname = name.lower()
        if lname in ['mpn1', 'mpn2']:
            field_map[name] = 'Designation'
        elif lname == 'designator':
            field_map[name] = 'Designator'
        elif lname == 'quantity':
            field_map[name] = 'Quantity'
        elif lname == 'case/package':
            field_map[name] = 'Footprint'
        else:
            field_map[name] = name.capitalize()

    output_headers = ['Id', 'Designator', 'Footprint', 'Quantity', 'Designation']

    rows = []
    for row in reader:
        if all(not v.strip() for v in row.values()):
            continue

        normalized_row = {}
        for k, v in row.items():
            key = field_map.get(k.strip().lower(), k)
            normalized_row[key] = v.strip()

        # Combine MPN1 and MPN2 into Designation, prefer MPN1
        if 'MPN1' in row and row['MPN1'].strip():
            normalized_row['Designation'] = row['MPN1'].strip()
        elif 'MPN2' in row:
            normalized_row['Designation'] = row['MPN2'].strip()
        else:
            normalized_row['Designation'] = ''

        rows.append(normalized_row)

# Merge entries with same Designation
merged = defaultdict(lambda: {"Designator": set(), "Footprint": "", "Quantity": 0, "Designation": ""})
preserved_rows = []

for row in rows:
    designation = row["Designation"].strip()
    if not designation:
        preserved_rows.append(row)
    else:
        merged[designation]["Designator"].update(map(str.strip, row["Designator"].split(",")))
        merged[designation]["Footprint"] = row.get("Footprint", "")
        merged[designation]["Quantity"] += int(row.get("Quantity", "0"))
        merged[designation]["Designation"] = designation

merged_rows = []
for idx, (designation, entry) in enumerate(merged.items(), start=1):
    merged_rows.append({
        "Id": str(idx),
        "Designator": ", ".join(sorted(entry["Designator"])),
        "Footprint": entry["Footprint"],
        "Quantity": str(entry["Quantity"]),
        "Designation": entry["Designation"]
    })

final_rows = merged_rows + preserved_rows

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=output_headers, delimiter=';')
    writer.writeheader()
    for idx, row in enumerate(final_rows, start=1):
        row["Id"] = idx
        writer.writerow(row)
