# crm/cron_jobs/clean_inactive_customers.sh
#!/bin/bash

# Change to project root
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
cd "$SCRIPT_DIR/../.."
cwd=$(pwd)

# Check if manage.py exists
if [ ! -f "$cwd/manage.py" ]; then
  echo "manage.py not found in $cwd. Exiting."
  exit 1
else
  echo "Running cleanup in $cwd"
fi

# Run Django shell command to delete inactive customers and log the result
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
DELETED=$(python manage.py shell <<EOF
from crm.models import Customer, Order
from datetime import datetime, timedelta

a_year_ago = datetime.now() - timedelta(days=365)
cust_ids = Customer.objects.exclude(order__order_date__gte=a_year_ago).distinct().values_list("id", flat=True)
deleted_count, _ = Customer.objects.filter(id__in=cust_ids).delete()
print(deleted_count)
EOF
)
echo "$TIMESTAMP - Deleted $DELETED inactive customers" >> /tmp/customer_cleanup_log.txt
