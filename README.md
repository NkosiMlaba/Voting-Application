# Voting-Application

## Project Status ![Status](https://img.shields.io/badge/status-completed-brightgreen)

1. The core functionality is completed

2. Additional features that I am looking to have implemented:
    - More robust user interface
    - Using databases to store the election data


## Account Requirements:
- A Google email
- A client_secret file from google cloud console <a href="#googlecloud">(instructions)</a>


## System Requirements:
- An internet connection
- A linux based machine
- Bash terminal
- Python3
- Pip
- .env file <a href="#encryption">(instructions)</a>


## Running instructions:
- Open terminal in the application's directory
- Run this command in terminal --> pip install -r dependencies/requirements.txt
    (installs the dependencies)
- Run this command in terminal --> 
    
        python3 project.py


## Testing instructions:
1. Command to run tests:
    
        python3 tests/test_project.py
        python3 tests/test_create.py
        python3 tests/test_participate.py
        python3 tests/test_view.py


## Key Features:
- Using Google Oauth to login and authenticate users
- Using Fernet to mask voter emails


## Detailed Description:
<p>
A voting app that can be used to host elections to gather data. Creating an election involves:
 naming the election, providing the number of candidates, entering information about each candidate, and answering whether the creator of the election is also allowed to vote and whether it is a public election or not. For non-public elections only specified people are allowed to vote.

 Viewing elections involves showing the user all available elections and prompting the user for the election they want to view. The user then enters the election number for the election they want to view. If there are no elections the user is returned to the previous screen. If the election is public any user can view the details of the election. If the election is private only the owner is allowed to view the details of the election. Details shown about the election include the title, whether the is allowed to vote, whether it is a public election, the election creator, the votes for each candidate, and the total votes in the election.

 Participating in an election involves showing the user available elections and then prompting the user for the election they wish to participate in. If there are no elections the user is returned to the previous screen. Based on the chosen election checks are made whether the user is allowed to vote in this election (the election may be private). If the user is not allowed to vote they are returned to the previous screen. If they are allowed to vote then the candidates are printed and the user is prompted for their choice. Once chosen the voting data is written and the scores are updated automatically.
</p>


## Encryption key instructions:
<p id=encryption>

1. Use this command to generate an encryption key:
    
        python3 encrypt/encryption.py
2. Create a .env file in the root of the directory and add the encryption key
</p>


## Obtaining client_secret:
<p id=googlecloud>

1. Create a Google Cloud Project:

    If you haven't already, navigate to the Google Cloud Console and create a new project. Note down the project ID.
    <br>
2. Set Up OAuth Consent Screen:
    Navigate to the "APIs & Services" > "OAuth consent screen" section.
    Configure the OAuth consent screen with required information such as the application name, user support email, and scopes. Make sure to include the following scope: "https://www.googleapis.com/auth/userinfo.email"
    Save your changes.
    <br>
3. Create OAuth 2.0 Client ID:
    Navigate to the "APIs & Services" > "Credentials" section.
    Click on the "Create credentials" button and select "OAuth client ID" from the dropdown menu.
    Choose the Desktop application.
    Click "Create" to generate your OAuth 2.0 Client ID and client secret.
    <br>
4. Download Client Secret File:
    After creating the OAuth 2.0 Client ID, you'll be provided with a client ID and client secret.
    Click on the download icon next to your client ID to download the client_secret.json file.
    Keep this file secure and do not share it publicly.
    <br>
5. Rename Client Secret File:
    Rename the file to "client_secret.json"
    <br>
6. Place Client Secret File in Project Directory:
    Once downloaded, move the "client_secret.json" file to the appropriate directory which is "VotingApp/authentication/"
    <br>
7. Configure the Project to Use Client Secret:
    The project is configured to run using the client_secret file in the authentication directory.
    <br>
8. Run the Project:
    With the client secret file properly configured, you can now run the project. Follow the project-specific instructions for setting up and running the application.
    <br>
</p>