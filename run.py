from app import create_app, db
from app.models import User, DDNSProvider
from flask_migrate import upgrade
from app.utils.scheduler import start_scheduler  # Import the start function
import json

app = create_app()

def initialize_database():
    with app.app_context():
        try:
            db.create_all()  # Ensure all tables are created
            User.create_admin()  # Create an admin user if one does not exist
            initialize_providers()  # Initialize DDNS providers
        except Exception as e:
            print("Error initializing the database: {}".format(e))
            raise

def initialize_providers():
    try:
        with open('approved_providers.json') as file:
            providers = json.load(file)

        for provider in providers:
            existing_provider = DDNSProvider.query.filter_by(name=provider['name']).first()
            if existing_provider:
                print("Provider '{}' already exists, skipping.".format(provider['name']))
            else:
                DDNSProvider.add_provider(provider['name'], provider['update_url'], provider['required_fields'])
                print("Provider '{}' added successfully.".format(provider['name']))
    except Exception as e:
        print("Error loading providers: {}".format(e))
        raise

# if __name__ == '__main__':
#     with app.app_context():
#         upgrade()  # Apply pending migrations
#         initialize_database()  # Initialize database
        
#         # Start the scheduler
#         start_scheduler(app)  # Pass the Flask app to the scheduler

#     app.run(host="0.0.0.0", port=5000, debug=True)  # Bind to 0.0.0.0 to make it accessible from outside

with app.app_context():
    upgrade()  # Apply pending migrations
    initialize_database()  # Initialize database

    # Start the scheduler when app starts
    start_scheduler(app)

# No app.run() as Gunicorn handles starting the app