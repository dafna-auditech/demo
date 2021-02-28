import base64
import os

from sendgrid import sendgrid
import csv
from sendgrid.helpers.mail import Content, Email, Mail, Personalization, Attachment, FileContent, FileName, FileType, \
    Disposition
import io
# from graph_tutorial import settings
from django.conf import settings
import jsonpickle as json

from .auth_helper import get_token
from .graph_helper import get_users


def send_users_control_email(request):
    users = get_users(request)
    stream = create_users_control_xlsx(users)

    to_email = ['amosg@audit-tech.net','eedry@audit-tech.net']
    subject = "Auditech user control - approve"
    content = Content("text/html charset=UTF-8",
                      "Attached the Users review control")
    encoded_file = base64.b64encode(stream).decode()
    
    attachment = Attachment(
        FileContent(encoded_file),
        FileName('ActiveDirectory-Control-report.xlsx'),
        FileType('application/xlsx'),
        Disposition('attachment'),
    )

    res = sendgird_send_email(to_email, subject, content, attachment)

    return res


def send_users_report_email(request):
    users = get_users(request)
    csv_stream = create_users_csv(users)
    stream = create_users_review_xlsx(users)

    to_email = ['amosg@audit-tech.net','eedry@audit-tech.net']
    subject = "Auditech user control - report"
    content = Content("text/html charset=UTF-8",
                      "Please review the attached users and approve the list,<br> notice the system "
                      "<a href='https://explore.auditech.xyz/approve'>click here to approve in Auditech system</a>"
                      "automatically filtered to show the users under your care."
    )


    encoded_xls = base64.b64encode(stream).decode()
    attachment_xlsx = Attachment(
        FileContent(encoded_xls),
        FileName('LA - Users Review - Screen-first_mail.xlsx'),
        FileType('application/xlsx'),
        Disposition('attachment'),
    )

    byte_stream = bytes(csv_stream.getvalue(), 'UTF-8')
    encoded_file = base64.b64encode(byte_stream).decode()
    
    attachment_raw = Attachment(
        FileContent(encoded_file),
        FileName('ActiveDirectory-users-report.csv'),
        FileType('application/csv'),
        Disposition('attachment'),
    )

    attachment = [attachment_raw,attachment_xlsx]
    res = sendgird_send_email(to_email, subject, content, attachment)

    return res


def sendgird_send_email(to, subject, content, attachment):
    import jsonpickle
    import base64

    SENDGRID_API_KEY = settings.SENDGRID_API_KEY
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)


    from_email = "amosg@audit-tech.net"

    mail = Mail(from_email=from_email, subject=subject, to_emails=to, plain_text_content=content)
    
    if type(attachment) == list:
        for att in attachment:
            mail.add_attachment(attachment=att)
    else:
        mail.add_attachment(attachment=attachment)

    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    # res = jsonpickle.dumps(mail, indent=4)
    return response


def create_users_csv(users):
    csv_stream: io.StringIo = io.StringIO()
    fieldnames = ['displayName', 'givenName', 'userPrincipalName', 'isIssue']
    writer = csv.DictWriter(csv_stream, fieldnames=fieldnames)
    writer.writeheader()
    for user in users['value']:
        u = {'displayName': user['displayName'],
             'givenName': user['givenName'],
             'userPrincipalName': user['userPrincipalName'],
             'isIssue': user.get('isIssue')
             }
        writer.writerow(u)
    return csv_stream


def create_users_control_xlsx(users):
    stream: io.BufferedReader = io.BytesIO
    with open('../resources/Product Demo Design - WP.xlsx','rb') as xl_file:
        return xl_file.read()

def create_users_review_xlsx(users):
    stream: io.BufferedReader = io.BytesIO
    with open('../resources/LA - Users Review - Screen-first_mail.xlsx','rb') as xl_file:
        return xl_file.read()


