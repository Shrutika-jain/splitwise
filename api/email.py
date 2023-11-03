from threading import Thread
from django.template.loader import render_to_string
from django.core.mail import BadHeaderError, EmailMessage
from http.client import HTTPResponse
from split_the_bill.settings import EMAIL_HOST_USER

class EmailThread(Thread):
    def __init__(self, subject, email_template, recipient_list, attachment_info = None):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = email_template
        self.attachment_info = attachment_info
        Thread.__init__(self)

    def run(self):
        for email in self.recipient_list:
            try:
                if not self.attachment_info==None:
                    mail = EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, [email])
                    try:
                        name = self.attachment_info[0]
                        content = self.attachment_info[1]
                        content_type = self.attachment_info[2]
                        mail.attach(filename=name, mimetype=content_type, content=content)
                    except Exception as e:
                        print("Error while attching the file", e)
                    mail.send()
                    print('Sent the email to', email)
                else:
                    EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, [email]).send()
            except BadHeaderError:
                return HTTPResponse('Invalid header found.')
        return True
    
# Function for sending email to user when a new expense is added
def send_expense_email(owe_from, owe_by, amount):
    subject = "New expense is added"
    email_template_name = "email/expense_added.txt"

    c = {
        "name": owe_by.get_full_name(),
        "amount": amount,
        "pay_to_user": owe_from.get_full_name()
    }
    email_template = render_to_string(email_template_name, c)
    recipient_list = [owe_by.email, ]
    EmailThread(subject, email_template, recipient_list).start()

# Function for sending email how much the user owe to each other
def send_weekly_email(user, data):
    subject = "Expense that you owe each other"
    email_template_name = "email/weekly_expense_report.txt"

    c = {
        "name": user.get_full_name(),
        "data": data
    }
    email_template = render_to_string(email_template_name, c)
    recipient_list = [user.email, ]
    EmailThread(subject, email_template, recipient_list).start()