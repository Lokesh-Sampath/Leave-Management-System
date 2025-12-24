from django.contrib import admin
from .models import LeaveBalance


@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_leaves', 'used_leaves')
