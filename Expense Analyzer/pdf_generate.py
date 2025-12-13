# generate_and_send_all_pdfs.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import smtplib
from email.message import EmailMessage
from email.mime.application import MIMEApplication

# Replace with actual emails
emails = {
    "SP": "",
    
}

def generate_person_pdf_in_memory(person, expenses):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"Expense Report for {person}")
    y = 720
    total = 0
    for entry in expenses:
        share = entry["Amount"] / entry["PersonCount"]
        total += share
        line = f"{entry['Date']}  {entry['Expences']}  {entry['Amount']}  {share:.2f}"
        c.drawString(100, y, line)
        y -= 20
    c.drawString(100, y - 10, f"Total Expenses for {person}: {total:.2f}")
    c.save()
    buffer.seek(0)
    return buffer

def send_email_with_pdf(person, pdf_buffer):
    msg = EmailMessage()
    msg['Subject'] = f"Expense Report for {person}"
    msg['From'] = ""  # Replace with real sender
    msg['To'] = emails[person]

    msg.set_content(f"Hi {person},\n\nAttached is your expense report.\n\nRegards.")

    pdf_data = pdf_buffer.read()
    msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=f"{person}_report.pdf")

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:  # Replace with real SMTP server
        smtp.starttls()
        smtp.login("", "")  
        smtp.send_message(msg)

    print(f"Email sent to {person}")

def generate_and_send_all_pdfs(data):
    persons = set()
    for entry in data:
        persons.update(entry["PersonList"])

    for person in persons:
        person_expenses = [e for e in data if person in e["PersonList"]]
        pdf_buffer = generate_person_pdf_in_memory(person, person_expenses)
        if person == 'SP':
            send_email_with_pdf(person, pdf_buffer)

