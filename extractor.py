import fitz  # PyMuPDF
import json

pdf_path = "Form ADT-1-29092023_signed.pdf"

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    full_text = ""
    for page in doc:
        full_text += page.get_text("text") + "\n"
    return full_text

def extract_keywords_simple(lines):
    data = {
        "cin": "",
        "company_name": "",
        "registered_office": "",
        "appointment_type": "",
        "auditor_name": "",
        "auditor_frn_or_membership": "",
        "auditor_address": "",
        "appointment_date": ""
    }

    # Find CIN (after 'Pre-fill' line)
    for i, line in enumerate(lines):
        if line == "Pre-fill" and i + 1 < len(lines):
            data["cin"] = lines[i+1].strip()
            if i + 2 < len(lines):
                data["company_name"] = lines[i+2].strip()
            break

    # Registered office (lines after company name until line containing 'Karnataka')
    if data["company_name"]:
        start = None
        for i, line in enumerate(lines):
            if line == data["company_name"]:
                start = i + 1
                break
        if start:
            address_parts = []
            for line in lines[start:]:
                if "Karnataka" in line:
                    break
                address_parts.append(line.strip())
            data["registered_office"] = ", ".join(address_parts).strip()

    # Appointment type (line containing 'Appointment/Re-appointment')
    for line in lines:
        if "Appointment/Re-appointment" in line:
            data["appointment_type"] = line.strip()
            break

    # Auditor name (look for known name)
    for i, line in enumerate(lines):
        if line.strip() == "MALLYA & MALLYA":
            data["auditor_name"] = "MALLYA & MALLYA"
            # Try to get FRN (next lines)
            if i + 1 < len(lines):
                if "001955S" in lines[i+1]:
                    data["auditor_frn_or_membership"] = "001955S"
            # Get auditor address (next few lines until Bangalore)
            addr = []
            for l in lines[i+1:]:
                addr.append(l.strip())
                if "Bangalore" in l:
                    break
            data["auditor_address"] = ", ".join(addr).strip()
            break

    # Appointment date (first line containing date in dd/mm/yyyy format)
    for line in lines:
        parts = line.split()
        for part in parts:
            if len(part) == 10 and part[2] == '/' and part[5] == '/':
                day, month, year = part.split('/')
                if day.isdigit() and month.isdigit() and year.isdigit():
                    data["appointment_date"] = part
                    break
        if data["appointment_date"]:
            break

    return data

def main():
    text = extract_text_from_pdf(pdf_path)
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    with open("extracted_text.txt", "w", encoding="utf-8") as f:
        f.write(text)

    data = extract_keywords_simple(lines)

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("✅ Extraction complete. Check output.json")

if __name__ == "__main__":
    main()
