# app/utils/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from app.models.ddns import DDNSConfig
from app.utils.ddns_updater import update_ddns
from datetime import datetime
from app import db
from app.models.logs import AppLog, DDNSUpdateLog

# Initialize the scheduler
scheduler = BackgroundScheduler()

def scheduled_ddns_updates():
    with scheduler.app.app_context():  # Use the app context
        configs = DDNSConfig.query.all()
        for config in configs:
            now = datetime.utcnow()

            if config.last_update_attempt:
                time_since_last_update = (now - config.last_update_attempt).total_seconds() / 60
            else:
                time_since_last_update = config.update_interval  # Treat as if it needs updating

            if time_since_last_update >= config.update_interval:
                success, message, ip = update_ddns(config)
                AppLog.create(level='INFO' if success else 'ERROR', message=message, module='scheduler')
                DDNSUpdateLog.create(
                    ddns_config_id=config.id,
                    success=success,
                    message=message + f" (Triggered by scheduler)",
                    ip_address=ip
                )

                print(f"Scheduled update for {config.provider.name}: {message}")

def start_scheduler(app):
    print("Scheduler start function called")  # Add logging here
    scheduler.app = app  # Attach the Flask app context to the scheduler
    scheduler.add_job(func=scheduled_ddns_updates, trigger="interval", minutes=1)
    scheduler.start()
    print("Scheduler started")  # Log scheduler startup
    AppLog.create(level='INFO', message='Scheduler started, checking DDNS updates every 1 minute.', module='scheduler')
