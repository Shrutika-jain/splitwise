from users.models import SplitAmoungUsers
from .email import send_expense_email

# Function to split the bill amoung user
def split_bill(amount_paid_by, owe_by, amount):
    
    # Check if the split instance exists when owe_from user that has paid the amount and owe_by user has tp pay the amount is same
    instance = SplitAmoungUsers.objects.filter(owe_from=amount_paid_by, owe_by=owe_by)
    if instance.exists():
        instance = instance.first()
        instance.amount = float(instance.amount) + float(amount)
        instance.save()

    # Check if the split instance exists when owe_from user that has paid the amount and owe_by user has tp pay the amount is not same
    else:
        instance = SplitAmoungUsers.objects.filter(owe_from=owe_by, owe_by=amount_paid_by)
        if instance.exists():
            instance = instance.first()
            if instance.amount > amount:
                instance.amount = instance.amount - amount
                instance.save()
            else:
                instance.amount = amount - instance.amount
                instance.owe_from = amount_paid_by
                instance.owe_by = owe_by
                instance.save()

        else:
            SplitAmoungUsers.objects.create(owe_from=amount_paid_by, owe_by=owe_by, amount=amount)

        # Send mail to user with amount
        # send_expense_email(amount_paid_by, owe_by, amount)
        
    return True

def passbook_data(user):
    # Amount that user has paid
    data = SplitAmoungUsers.objects.filter(owe_from=user, amount__gte=0)
    amount_paid = []
    total_amount_paid = 0
    for data in data:
        print("data", data)
        total_amount_paid += data.amount 
        amount_paid.append({
            "owe_by_userid": data.owe_by.userid,
            "owe_by_name": data.owe_by.get_full_name(),
            "amount": data.amount,
            "date": data.created_at.date()
        })

    # Amount that user has to pay
    data = SplitAmoungUsers.objects.filter(owe_by=user, amount__gte=0)
    payable_amount = []
    total_payable_amount = 0
    for data in data:
        print("data", data)
        total_payable_amount += data.amount 
        payable_amount.append({
            "pay_to_userid": data.owe_from.userid,
            "pay_to_name": data.owe_from.get_full_name(),
            "amount": data.amount,
            "date": data.created_at.date()
        })

    if total_amount_paid > total_payable_amount:
        message = f"{user.get_full_name()} has to take {total_amount_paid - total_payable_amount} to users."
    else:
        message = f"{user.get_full_name()} has to pay {total_payable_amount - total_amount_paid} to users."

    response = {
        "message": "Here is the list of how much amount user has to take and pay to other users.",
        "success": True,
        "passbook": {
            "overall_result": message,
            "total_amount_paid": total_amount_paid,
            "amount_paid": amount_paid,
            "total_payable_amount": total_payable_amount,
            "payable_amount": payable_amount
        }
    }
    return response


