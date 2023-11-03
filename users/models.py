from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(AbstractUser):
    userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    mobile_number = PhoneNumberField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class SplitAmoungUsers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owe_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owe_from")  # User that paid the amount
    owe_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owe_by")  # User that has to pay thr amount
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    created_at = models.DateTimeField(auto_now=True, auto_created=True)

    class Meta:
        unique_together = (
            "owe_from",
            "owe_by",
        )

    def __str__(self):
        return f"{self.owe_from} owes {self.owe_by}: Rs {self.amount}"
    