import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup


TOKEN=os.getenv("TOKEN")


headers = { 
    "Authorization": f"Bearer {TOKEN}" 
}

seen_ids = set()

# Display an individual email
def display_email(email_id, headers):
    email_url = f'https://smails.dev/api/mailbox/messages/{email_id}'

    try:
        get_email = requests.get(email_url, headers=headers, timeout=(3,10))
        get_email.raise_for_status()

        email_data = get_email.json()

    except requests.exceptions.JSONDecodeError as e:
        print(f'JSON DECODE ERROR: {e}')
        return False
    except requests.exceptions.RequestException as e:
        print(f'There was an error: {e}')
        return False

    print(f'From: {email_data.get('from_name', 'Unknown sender')}')
    print(f"Email: {email_data.get('from_addr', 'Unknown address')}")
    print(f"Subject: {email_data.get('subject', '(No subject)')}")

    # Put time into a readable format
    timestamp = email_data.get('received_at')

    if timestamp:
        received_at = datetime.fromtimestamp(timestamp / 1000)
        print(f"Received At: {received_at.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("Received At: Unknown")

    email_body = email_data.get('text')
    # If the email body is in HTML Format:
    email_body_html = email_data.get('html')

    if email_body and email_body.strip():
        print(email_body)
    elif email_body_html and email_body_html.strip():
        soup = BeautifulSoup(markup=email_body_html, features='html.parser')
        print(f"{soup.get_text(separator='\n', strip=True)}")
    else:
        print("This email has no readable body.")
    print("-" * 50)






# Get inbox
def display_inbox(headers, seen_ids): 
    try:
        response = requests.get("https://smails.dev/api/mailbox/messages", headers=headers, timeout=(3,10))

        response.raise_for_status()

        emails = response.json()

        print(emails)

    except requests.exceptions.RequestException as e:
        print(f'Could not check inbox: {e}')
        return False

    except requests.exceptions.JSONDecodeError as e:
        print(f'Invalid inbox response: {e}')
        return False

    for email in emails:
        email_id = email.get('id')

        if email_id and email_id not in seen_ids:
            display_email(email_id, headers);
            seen_ids.add(email_id)



try:
    req = requests.post('https://smails.dev/api/mailbox', timeout=(3,10))

    data = req.json()

    if isinstance(data, dict):
        if 'address' in data and 'token' in data:
            email = data['address']
            token = data['token']
            




    display_inbox()


except requests.exceptions.RequestException as e:
    print(f"There was an error with the request: {e}")