# CRM Project Setup Guide

## Setup
1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run Migrations**:
```bash
python manage.py migrate
```

3. **Start Redis**:
```bash
redis-server
```

4. **Start Celery Worker**:
```bash
celery -A alx_backend_graphql_crm worker -l info
```

5. **Start Celery Beat Scheduler**:
```bash
celery -A alx_backend_graphql_crm beat -l info
```

6. **Verify Logs**:
```
cat /tmp/crm_report_log.txt
```