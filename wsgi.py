from app import create_app
from app.utils.scheduler import start_scheduler

app = create_app()

if __name__ != "__main__":
    with app.app_context():
        start_scheduler(app)  # Start the scheduler in the master process
