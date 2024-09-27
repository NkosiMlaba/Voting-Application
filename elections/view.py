import os
import json

# Declaration section
current_directory = os.getcwd()
subdirectory_path = os.path.join(current_directory, "database")


def get_elections():
    """
    This function retrieves a list of elections from the database directory.
    
    Parameters:
    None
    
    Returns:
    elections (list): A list of election names.
    """
    elections = sorted(os.listdir(subdirectory_path))
    for election in elections:
        print(election)
    return elections


def get_chosen_election(elections):
    """
    This function prompts the user to select an election from the given list.
    
    Parameters:
    elections (list): A list of election names.
    
    Returns:
    election (str): The name of the chosen election.
    """
    while True:
        election_number = input("Enter the poll / election number: ")
        try:
            election_number = int(election_number)
            election = elections[election_number-1]
            return election
        except:
            continue


def read_meta_data(chosen_election):
    """
    This function reads the metadata of a chosen election from a JSON file.
    
    Parameters:
    chosen_election (str): The name of the chosen election.
    
    Returns:
    data (dict): The metadata of the chosen election.
    """
    meta_data = os.path.join(subdirectory_path, chosen_election, "metadata.json")
    with open(meta_data, 'r') as file:
        data = json.load(file)
    return data


def is_allowed_to_view(user_email, chosen_election):
    """
    This function checks if a user is allowed to view the metadata of a chosen election.
    
    Parameters:
    user_email (str): The email of the user.
    chosen_election (str): The name of the chosen election.
    
    Returns:
    bool: True if the user is allowed to view the election, False otherwise.
    """
    meta_data = read_meta_data(chosen_election)
    
    if user_email == meta_data["creator"]:
        return True
    elif meta_data["voters"] == ["everyone"]:
        return True
    
    return False


def print_election_title(chosen_election):
    """
    This function prints the title of a chosen election.
    
    Parameters:
    chosen_election (dict): The metadata of the chosen election.
    """
    print()
    title = chosen_election["title"]
    print(f"The title of this election is: \n        {title}")
    print()


def print_votes(chosen_election):
    """
    This function prints the number of votes for each option in a chosen election.
    
    Parameters:
    chosen_election (dict): The metadata of the chosen election.
    """
    total_votes = 0
    
    for option, votes in chosen_election["election_data"].items():
        print(f"{votes} vote(s) for: {option.capitalize()}.")
        total_votes += votes
    print()
    print(f"Total votes for this election: \n        {total_votes}")
    print()


def print_is_self_voting(chosen_election):
    """
    This function prints whether the creator of the election is allowed to vote.
    
    Parameters:
    chosen_election (dict): The metadata of the chosen election.
    """
    selfvoting = chosen_election["self_voting"]
    print(f"Is the maker of the election allowed to vote?: \n        {selfvoting}")
    print()


def print_is_public_election(chosen_election):
    """
    This function prints whether the election is public or not.
    
    Parameters:
    chosen_election (dict): The metadata of the chosen election.
    """
    is_public = chosen_election["public_election"]
    print(f"Is this a public election: \n        {is_public}")
    print()


def print_election_creator(chosen_election):
    """
    This function prints the email of the creator of the election.
    
    Parameters:
    chosen_election (dict): The metadata of the chosen election.
    """
    creator = chosen_election["creator"]
    print(f"The creator of this election is: \n        {creator}")
    print()


def print_voters(chosen_election):
    """
    This function prints the list of people allowed to vote in the election.
    
    Parameters:
    chosen_election (dict): The metadata of the chosen election.
    """
    voters = chosen_election["voters"]
    print(f"People allowed to vote in: \n        {voters}")
    print()
    