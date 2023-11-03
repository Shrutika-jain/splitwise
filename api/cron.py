from users.models import User
from .utils import passbook_data
from .email import send_weekly_email

# Function to schedule weekly email of amount users owe to each other
def schedule_expense_email():
    users = User.objects.all() 
    for user in users:
        data = passbook_data(user)
        send_weekly_email(user, data)
    return True