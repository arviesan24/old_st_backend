import sendgrid
from decouple import config
from sendgrid.helpers.mail import *

from components.database.users import search_doctor
from components.utils.email_template import template_text


def send_email(doctor, appointment):
    sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
    from_email = Email("ctechnology24@gmail.com")
    subject = "New Appointment"
    doctor_email = search_doctor(doctor)['email']
    to_email = To(doctor_email)
    accepted = 'Yes' if appointment['accepted'] else 'No'
    comment = appointment['comment'] if appointment['comment'] else ''
    content = Content("text/plain", template_text.format(
        doctor=doctor.capitalize(),
        date=appointment['date'],
        start=appointment['start'],
        end=appointment['end'],
        patient=appointment['patient_name'],
        accepted=accepted,
        comment=comment))
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
