import requests
from datetime import datetime
from app.models import db
from app.models.logs import AppLog, DDNSUpdateLog

def get_current_ip():
    try:
        # Get the current external IP using a service like ipify
        response = requests.get('https://api.ipify.org')
        return response.text.strip()
    except requests.RequestException as e:
        AppLog.create(level='ERROR', message=f"Failed to get current IP: {str(e)}", module='ddns_updater')
        return None

def update_ddns(config):
    # Fetch the current external IP address
    current_ip = get_current_ip()
    config.last_update_attempt = datetime.utcnow()
    config.current_ip = current_ip

    if not current_ip:
        db.session.commit()
        AppLog.create(level='ERROR', message="Failed to get current IP", module='ddns_updater')
        return False, "Failed to get current IP", None

    # Construct parameters for the DuckDNS API (ensure we use 'domains' and 'token')
    params = {
        'domains': config.config_values['domain'],  # Use 'domains' for DuckDNS
        'token': config.config_values['token'],
        'ip': current_ip
    }

    try:
        # Log the outgoing request
        print(f"Sending request to {config.provider.update_url} with params: {params}")

        # Send the GET request
        response = requests.get(config.provider.update_url, params=params)
        
        # Log the response for debugging
        with open('response.txt', 'w') as f:
            f.write(response.text)

        # Check if the response is valid
        if response.status_code == 200 and response.text.strip().lower() == 'ok':
            config.last_successful_update = datetime.utcnow()
            message = f"DDNS updated successfully. IP: {current_ip}"
            AppLog.create(level='INFO', message=message, module='ddns_updater')
            # DDNSUpdateLog.create(
            #     ddns_config_id=config.id,
            #     success=True,
            #     message=message,
            #     ip_address=current_ip
            # )
        else:
            message = f"DDNS update failed. Response: {response.text}"
            AppLog.create(level='ERROR', message=message, module='ddns_updater')

        # Commit the result to the database
        db.session.commit()

        return True, message, current_ip

    except requests.RequestException as e:
        # Handle request failures
        error_message = f"DDNS update request failed: {str(e)}"
        AppLog.create(level='ERROR', message=error_message, module='ddns_updater')
        db.session.commit()
        return False, error_message, current_ip
