import json

import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup

import websocket

URL = "https://smails.dev/api/mailbox"




# Display an individual email
def display_email(email_id, headers):
    email_url = f'{URL}/messages/{email_id}'

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

    print(f"From: {email_data.get('from_name', 'Unknown sender')}")
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
        response = requests.get(f"{URL}/messages", headers=headers, timeout=(3,10))

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
            display_email(email_id, headers)
            seen_ids.add(email_id)


def main():
    try:
        req = requests.post(URL, timeout=(3,10))
        req.raise_for_status()
        data = req.json()

        if isinstance(data, dict):
            if 'address' in data and 'token' in data:
                email = data['address']
                token = data['token'] 
                if isinstance(email, str) and isinstance(token, str) and bool(email) and bool(token):
                    print(f'Your email is {email}')
                    # copy_to_clipboard(email)
                    print('Email copied to clipboard')

                    headers = { 
                        "Authorization" : f'Bearer {token}'
                    }



                    seen_ids = set()
                    ws_url = f"wss://smails.dev/api/mailbox/connect?token={token}"
                    ws = websocket.WebSocket()

                    try:
                        ws.connect(ws_url, timeout=300)
                        ws.settimeout(1)
                        print("Websocket connected")

                        while True:
                            try:
                                event = ws.recv()
                            except websocket.WebSocketTimeoutException:
                                continue

                            try:
                                event_data = json.loads(event)
                            except json.JSONDecodeError:
                                print("Received an invalid event")
                                continue

                            if event_data.get('type') == 'new_message':
                                message_id = event_data.get('id')

                                if message_id and message_id not in seen_ids:
                                    if display_email(message_id, headers):
                                        seen_ids.add(message_id)
                            
                    except KeyboardInterrupt:
                        print("Stopping WebSocket connection")

                    except websocket.WebSocketException as e:
                        print(f"WebSocket error: {e}")

                    finally:
                        ws.close()


    except requests.exceptions.RequestException as e:
        print(f"There was an error with the request: {e}")



if __name__ == "__main__":
    main()