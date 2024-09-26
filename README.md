# DDNS Manager

DDNS Manager is a Flask-based web application designed to manage and update Dynamic DNS (DDNS) configurations. It provides a user-friendly interface for managing multiple DDNS providers and configurations, with a focus on DuckDNS.

## Features

- User authentication and authorization
- Dashboard for viewing and managing DDNS configurations
- Manual and automatic DDNS updates
- Logging of update attempts and results
- Email notifications for update status (configurable)
- Admin interface for global settings and logs

## Project Structure

```
ddns-manager/
├── app/
│   ├── models/
│   │   ├── user.py
│   │   ├── ddns.py
│   │   ├── logs.py
│   │   └── notification.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── ddns.py
│   │   ├── logs.py
│   │   └── notification.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   │   ├── auth/
│   │   ├── ddns/
│   │   └── notification/
│   ├── utils/
│   │   ├── ddns_updater.py
│   │   └── notification_sender.py
│   └── __init__.py
├── config.py
├── run.py
├── requirements.txt
└── .env
```

## Key Components

### Models

- `User`: Handles user authentication and roles
- `DDNSConfig`: Stores DDNS configuration details
- `DDNSProvider`: Defines supported DDNS providers
- `AppLog`: General application logging
- `DDNSUpdateLog`: Logs DDNS update attempts and results
- `NotificationSettings`: Manages email notification settings

### Routes

- `auth`: Handles user registration, login, and logout
- `ddns`: Manages DDNS configurations, updates, and the dashboard
- `logs`: Provides access to application and DDNS update logs
- `notification`: Manages notification settings and preferences

### Utils

- `ddns_updater`: Contains the logic for updating DDNS records
- `notification_sender`: Handles sending email notifications

## Setup and Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.template` to `.env` and fill in the required values
6. Initialize the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```
7. Run the application: `python run.py`

## Usage

1. Register a new user account or log in with existing credentials
2. Add DDNS configurations through the settings page
3. View and manage DDNS configurations on the dashboard
4. Manually trigger DDNS updates or let the automatic updates handle it
5. Configure notification preferences in the user settings
6. Admins can access additional settings and logs

## Configuration

The application uses environment variables for configuration. Key settings include:

- `SECRET_KEY`: Used for session management
- `DATABASE_URL`: Database connection string
- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD`: Email server settings

## Planned Improvements

1. Support for additional DDNS providers (e.g., No-IP, Dynu)
2. Implement a background task scheduler for automatic DDNS updates
3. Add two-factor authentication for enhanced security
4. Create a RESTful API for programmatic access to DDNS management
5. Implement a mobile-friendly responsive design
6. Add support for IPv6 DDNS updates
7. Implement user groups for shared DDNS management
8. Add support for custom DDNS providers with user-defined update URLs
9. Implement a dark mode for the user interface
10. Add support for importing/exporting DDNS configurations
11. Implement rate limiting for DDNS updates to prevent abuse
12. Add support for webhook notifications
13. Implement a status page showing the health of DDNS services
14. Add support for DNS record management beyond just A records
15. Implement a plugin system for easy extension of functionality

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.