import requests
from bs4 import BeautifulSoup
import os

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

def display_inbox(): 
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



try:
    # req = requests.post('https://smails.dev/api/mailbox', timeout=(3,10))

    # data = req.json()



    display_inbox()


except requests.exceptions.RequestException as e:
    print(f"There was an error with the request: {e}")