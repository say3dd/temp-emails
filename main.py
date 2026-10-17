import requests

TOKEN = "placeholder"
headers = { 
    "Authorization": f"Bearer {TOKEN}" 
}

def display_inbox(): 
    try:
        response = requests.get("https://smails.dev/api/mailbox/messages", headers=headers, timeout=(3,10))

        emails = response.json()

        print(emails)

    except requests.exceptions.RequestException as e:
        print(f'Could not check inbox: {e}')
        return False

    except requests.exceptions.JSONDecodeError as e:
        print(f'Invalid inbox response: {e}')
        return False


try:
    req = requests.post('https://smails.dev/api/mailbox', timeout=(3,10))

    data = req.json()


    display_inbox()


except requests.exceptions.RequestException as e:
    print(f"There was an error with the request: {e}")