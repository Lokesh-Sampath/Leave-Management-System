from django.db import models

from django.contrib.auth.models import User


class LeaveRequest(models.Model):
    
    LEAVE_TYPE_CHOICES = (
        ('CASUAL',"Causal Leave"),
        ('SICK', "Sick Leave"),
        ('PAID',"Paid Leave")
    )
    
    STATUS_CHOICE = (
         ('APPROVED',"Approved"),
         ('PENDING',"Pending"),
         ('REJECTED',"Rejected")
    )
    
    employee = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name = "leave_request"
    )
    
    leave_type= models.CharField(
        max_length=20,
        choices= LEAVE_TYPE_CHOICES
        
    )
    
    start_date = models.DateField()
    
    end_date = models.DateField()
    
    reason = models.TextField(
        null = True,
        blank = True
    )
    
    status = models.CharField(
        max_length=10,
        choices= STATUS_CHOICE,
        default = "PENDING"
    )
    
    approved_by = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        blank = True,
        null= True,
        related_name='approved_leaves'
    )
    
    rejection_reason = models.TextField(
        blank = True,
        null = True
    )
    
    created_at = models.DateTimeField(
           auto_now_add= True
    )
    
    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} - {self.status}"
    


class LeaveBalance(models.Model):
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="leave_balance"
    )
    
    total_leaves = models.IntegerField()
    used_leaves = models.IntegerField()    
    
    def remaining_leave(self):
        return self.total_leaves - self.used_leaves
    
    def __str__(self):
        return f"{self.user.username} - Remaining:{self.remaining_leave()}"
    