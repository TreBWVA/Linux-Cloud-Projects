# Open crontab editor
crontab -e

# Add entry to execute daily at 8:00 PM
0 20 * * * /opt/azure-monitor/venv/bin/python /opt/azure-monitor/auto_shutdown.py >> /var/log/azure_shutdown.log 2>&1