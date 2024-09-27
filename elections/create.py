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
    """Creates a new election directory and stores the election information.
    Args:
        title (str): The title of the election.
        options_and_data (dict): A dictionary containing the options and their corresponding data.
        allow_self_voting (bool): Whether the creator of the election is allowed to vote.
        is_public_election (bool): Whether the election is open to the public.
        email (str): The email address of the election creator.
        voters_list (list): A list of email addresses of eligible voters.
    """
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
    """Counts the number of directories in the database subdirectory.

    Returns:
        int: The number of directories.
    """
    directory = subdirectory_path
    items = os.listdir(directory)
    num_directories = 0
    
    for item in items:
        if os.path.isdir(os.path.join(directory, item)):
            num_directories += 1
    
    return num_directories


def get_election_title():
    """Prompts the user to enter the title of the election.

    Returns:
        str: The title of the election.
    """
    
    while True:
        title = input("Enter the name of your election: \n        ")
        if title != "":
            return title


def get_options_number():
    """Prompts the user to enter the number of options.

    Returns:
        int: The number of options.
    """
    
    while True:
        number = input("Enter number of available options: \n        ")
        try:
            number = int(number)
            if number < 2:
                continue
            return number
        except:
            continue


def get_option(number):
    """Prompts the user to enter the name of an option.

    Args:
        number (int): The option number.

    Returns:
        str: The name of the option.
    """
    while True:
        option = input(f"Enter the name of the {number} option in the election: \n        ")
        if option != "":
            return option


def get_data(option):
    """Prompts the user to enter details for an option.

    Args:
        option (str): The option name.

    Returns:
        str: The details for the option.
    """
    while True:
        data = input(f"Enter the enter all details corresponding to {option} option in the election: \n        ")
        if data != "":
            return data


def get_options_details(number_of_options):
    """Gets the details for all options in the election.

    Args:
        number_of_options (int): The number of options.

    Returns:
        dict: A dictionary containing the options and their details.
    """

    options_and_data = {}
    for number in range(1, number_of_options+1):
        option = get_option(number)
        candidate_data = get_data(option)
        options_and_data[option] = candidate_data
    
    return options_and_data


def get_is_self_voting():
    """Asks the user if they are allowed to vote in the election.

    Returns:
        bool: True if self-voting is allowed, False otherwise.
    """
    
    while True:
        print("As the maker of this election, are you allowed to participate in it?\n        ")
        is_owner_voting = input(f"Enter 'Yes' to allow self voting and 'No' to disallow it: ")
        if is_owner_voting.lower() == "yes":
            return True
        
        elif is_owner_voting.lower() == "no":
            return False


def get_is_public_election():
    """Asks the user if the election is public or private.

    Returns:
        bool: True if the election is public, False otherwise.
    """
    while True:
        print("Is this a public election (anyone can participate) or private")
        is_public = input(f"Enter 'Yes' for public election and 'No' for a private: ")
        if is_public.lower() == "yes":
            return True
        
        elif is_public.lower() == "no":
            return False


def get_voters_number():
    """Prompts the user to enter the number of eligible voters.

    Returns:
        int: The number of eligible voters.
    """
    while True:
        number = input("Enter number of people you want to be able to vote in the election: ")
        try:
            number = int(number)
            return number
        except:
            continue


def get_voter_email(number):
    """Prompts the user to enter the email address of a voter.

    Args:
        number (int): The voter number.

    Returns:
        str: The email address of the voter.
    """
    while True:
        data = input(f"Enter the email corresponding to {number} voter in the election: \n        ")
        if data != "":
            return data


def get_allowed_voters(is_public_election):
    """Gets the list of eligible voters for the election.

    Args:
        is_public_election (bool): Whether the election is public or private.

    Returns:
        list: A list of email addresses of eligible voters.
    """
    if is_public_election:
        return ["everyone"]
    
    voters_total = get_voters_number()
    voter_emails = []
    for number in range(1, voters_total+1):
        voter = get_voter_email(number)
        voter_emails.append(voter)
    
    return voter_emails
