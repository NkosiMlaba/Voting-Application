import os
import json

# Declaration section
current_directory = os.getcwd()
subdirectory_path = os.path.join(current_directory, "database")


def create_election(title,
                    options_and_data,
                    allow_self_voting,
                    is_public_election,
                    email,
                    voters_list):
    
    vote_data_default = {}
    for option in options_and_data.keys():
        vote_data_default[option] = 0



    election_metadata = {"title": title,
                         "election_data": vote_data_default,
                         "self_voting": allow_self_voting,
                         "public_election": is_public_election,
                         "creator": email,
                         "voters": voters_list
                         }


    
    directory_number_available = count_directories() + 1
    election_path = f"{subdirectory_path}/{directory_number_available}.{title}"
    os.makedirs(election_path, exist_ok=True)

    metadata_path = os.path.join(election_path, 'metadata.json')
    with open(metadata_path, 'w') as file:
        json.dump(election_metadata, file)

    voter_data_path = os.path.join(election_path, 'voter_data.txt')
    with open(voter_data_path, "wb") as file:
        pass

    options_data_path = os.path.join(election_path, 'option_data.json')
    with open(options_data_path, 'w') as file:
        json.dump(options_and_data, file)
    


def count_directories():
    directory = subdirectory_path
    items = os.listdir(directory)
    num_directories = 0
    
    for item in items:
        if os.path.isdir(os.path.join(directory, item)):
            num_directories += 1
    
    return num_directories


def get_election_title():
    
    while True:
        title = input("Enter the name of your poll / election: ")
        if title != "":
            return title


def get_options_number():
    
    while True:
        number = input("Enter number of candidates /options: ")
        try:
            number = int(number)
            if number < 2:
                continue
            return number
        except:
            continue


def get_option(number):
    while True:
        option = input(f"Enter the name of the {number} option in the election: ")
        if option != "":
            return option


def get_data(option):
    while True:
        data = input(f"Enter the enter all details corresponding to {option} option in the election: ")
        if data != "":
            return data


def get_options_details(number_of_options):

    options_and_data = {}
    for number in range(1, number_of_options+1):
        option = get_option(number)
        candidate_data = get_data(option)
        options_and_data[option] = candidate_data
    
    return options_and_data


def get_is_self_voting():
    
    while True:
        print("As the maker of this election, are you allowed to participate in it?")
        is_owner_voting = input(f"Enter 'Yes' to allow self voting and 'No' to disallow it: ")
        if is_owner_voting.lower() == "yes":
            return True
        
        elif is_owner_voting.lower() == "no":
            return False


def get_is_public_election():

    while True:
        print("Is this a public election (anyone can participate) or private")
        is_public = input(f"Enter 'Yes' for public election and 'No' for a private: ")
        if is_public.lower() == "yes":
            return True
        
        elif is_public.lower() == "no":
            return False


def get_voters_number():
    while True:
        number = input("Enter number of people you want to be able to vote in the election: ")
        try:
            number = int(number)
            return number
        except:
            continue


def get_voter_email(number):
    while True:
        data = input(f"Enter the email corresponding to {number} voter in the election: ")
        if data != "":
            return data


def get_allowed_voters(is_public_election):
    if is_public_election:
        return ["everyone"]
    
    voters_total = get_voters_number()
    voter_emails = []
    for number in range(1, voters_total+1):
        voter = get_voter_email(number)
        voter_emails.append(voter)
    
    return voter_emails
