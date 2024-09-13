import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import requests

# Declaration section
CLIENT_SECRET_FILE = "authentication/client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/userinfo.email", "openid", ]


def authenticate():
    """Attempts to log in a user using their google account in browser"""
    creds = None
    
    try:
        if os.path.exists("authentication/token.json"):
            creds = Credentials.from_authorized_user_file("authentication/token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                        CLIENT_SECRET_FILE, SCOPES
                    )
                creds = flow.run_local_server(port=0)
                with open("authentication/token.json", "w") as token:
                    token.write(creds.to_json())
    except Exception as e:
        print("Failed to log in")
        print()
        exit(e)
    print("Authentication successful!")
    print()
    return creds


def get_user_data(creds):
    "Tries to get the user's email using the generated creds"
    try:
        userinfo_url = 'https://openidconnect.googleapis.com/v1/userinfo'
        
        response = requests.get(
            userinfo_url,
            headers={'Authorization': 'Bearer ' + creds.token}
        )
        if response.status_code == 200:
            user_info = response.json()
            email = user_info.get('email')
            print(f"User logged in: {email}")
            print()
            return email
        else:
            print("Error retrieving user info. Status code:", response.status_code)
            exit()
    except Exception as e:
        print("Failed to retrieve email")
        print()
        exit()
        

