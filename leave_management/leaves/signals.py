from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import LeaveBalance
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_leave_balance(sender, instance, created, **kwargs):
    if created:
         LeaveBalance.objects.create(
            user=instance,
            total_leaves = 20,
            used_leaves = 0,
          )
         
         