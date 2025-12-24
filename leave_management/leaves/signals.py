from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import LeaveBalance
from django.dispatch import receiver
from users.models import UserProfile

@receiver(post_save, sender=UserProfile)
def create_leave_balance(sender, instance, created, **kwargs):
    if created and instance.role == "EMPLOYEE":
         LeaveBalance.objects.create(
            user=instance.user,
            total_leaves = 20,
            used_leaves = 0,
          )
         
         
         