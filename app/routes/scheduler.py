# app/routes/scheduler.py
from flask import Blueprint, jsonify
from flask_login import login_required
from app.utils.scheduler import scheduler

scheduler_bp = Blueprint('scheduler', __name__)

@scheduler_bp.route('/scheduler_status', methods=['GET'])
@login_required
def scheduler_status():
    # Check if any jobs are scheduled
    jobs = scheduler.get_jobs()
    if jobs:
        return jsonify({"status": "Scheduler is running", "jobs": [job.id for job in jobs]}), 200
    else:
        return jsonify({"status": "Scheduler is not running or has no jobs"}), 500
