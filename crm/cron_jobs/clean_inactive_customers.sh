#!/bin/bash
# Script to clean inactive customers

cd "$(dirname "$0")/../.."  # نرجع لروت المشروع

deleted_count=$(python3 manage.py shell -c "
import sys
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(last_order_date__lt=cutoff)
count = qs.count()
qs.delete()
print(count)
")

echo \"$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $deleted_count\" >> /tmp/customer_cleanup_log.txt
