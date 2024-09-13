import os
import sys
import json

from elections import view
from encrypt import encryption

# Declaration section
current_dir = os.path.dirname(os.path.abspath(__file__))
one_level_up = os.path.abspath(os.path.join(current_dir, '../'))

encryption_path = os.path.join(one_level_up, "encrypt")
voter_data_path = os.path.join(one_level_up, "database")

sys.path.append(voter_data_path)
sys.path.append(encryption_path)


def is_allowed_to_vote(user_email, chosen_election):
    """
    Checks if the given user is allowed to vote in the specified election.
    
    Args:
        user_email (str): The email address of the user.
        chosen_election (str): The name of the election.
    
    Returns:
        bool: True if the user is allowed to vote, False otherwise.
    """
    meta_data = view.read_meta_data(chosen_election)

    voters = read_vote_data(chosen_election)

    if user_email == meta_data["creator"] and meta_data["self_voting"] == "false":
        print("You do not have permission participate in this election")
        print()
        return False
    
    if user_email in meta_data["voters"] or meta_data["voters"] == ["everyone"]:
        pass
    else:
        print("You do not have permission participate in this election!")
        print()
        return False

    if user_email in voters:
        print("You have already voted in this election!")
        print()
        return False
    
    return True


def read_vote_data(chosen_election):
    """
    Reads the voter data for the specified election from the voter data file.
    
    Args:
        chosen_election (str): The name of the election.
    
    Returns:
        list: A list of voter email addresses that have voted in the specified election.
    """
    voter_file = os.path.join(voter_data_path, chosen_election, 'voter_data.txt')

    try:
        with open(voter_file, "rb") as file:
            new_file = file.readlines()

    except Exception as e:
        print(e)
        exit("Exception found when trying to open voter data file")
    
    voters = []
    for voter_data in new_file:
        voter = encryption.decrypt_email(voter_data)
        voters.append(voter)
    
    return voters


def read_candidate_data(chosen_election):
    """
    Reads the candidate data for the specified election from the option data file.
    
    Args:
        chosen_election (str): The name of the election.
    
    Returns:
        dict: A dictionary containing the candidate data for the specified election.
    """
    meta_data = os.path.join(voter_data_path, chosen_election, "option_data.json")
    with open(meta_data, 'r') as file:
        data = json.load(file)
    return data


def get_candidates(chosen_election):
    """
    Retrieves the list of candidates and their additional information for the specified election.
    
    Args:
        chosen_election (str): The name of the election.
    
    Returns:
        list: A list of lists, where each inner list contains the candidate name and additional information.
    """
    candidate_data = read_candidate_data(chosen_election)

    candidates = []
    for option, additional_infromation in candidate_data.items():
        candidates.append([option, additional_infromation])
    
    return candidates


def prompt_for_option(candidate_list):
    """
    Prompts the user to select an option from a list of candidates and their additional information.
    
    Args:
        candidate_list (list): A list of lists, where each inner list contains the candidate name and additional information.
    
    Returns:
        int: The index of the selected option, where the index is 1-based (i.e., the first option is 1, not 0).
    """
    # [[], []]
    for index, option in enumerate(candidate_list):
        print()
        print(f"{index+1}. {option[0]}")
        print(f"Additional Information: {option[1]}.")
        print()
    
    while True:
        chosen_option_number = input("Enter the option / candidate number you wish to vote for: ")
        try:
            chosen_option_number = int(chosen_option_number)
            if chosen_option_number <= 0 or chosen_option_number > len(candidate_list):
                continue
            return chosen_option_number
        except:
            continue


def write_vote(chosen_election, email, option_chosen):
    """
    Writes the user's vote for the specified election to the voter data file.
    
    Parameters:
        chosen_election (str): The name of the election for which the vote is being recorded.
        email (str): The email address of the voter.
        option_chosen (str): The option or candidate that the voter has chosen.
    """
    voter_file = os.path.join(voter_data_path, chosen_election, 'voter_data.txt')

    encrypted_email = encryption.encrypt_email(email)
    with open(voter_file, "ab") as file:
        file.write(encrypted_email + b'\n')


def get_secret_email(email):
    """
    Encrypts the given email address using the encryption module.
    
    Args:
        email (str): The email address to be encrypted.
    
    Returns:
        str: The encrypted email address.
    """
    return encryption.encrypt_email(email)


def update_vote_score(chosen_election, option ):
    """
    Updates the vote score for a specific option in the chosen election.

    Parameters:
    chosen_election (str): The name of the election for which the vote score needs to be updated.
    option (str): The option for which the vote score needs to be updated.
    """
    meta_data = view.read_meta_data(chosen_election)

    meta_data["election_data"][option] += 1

    meta_data_path = os.path.join(voter_data_path, chosen_election, "metadata.json")
    with open(meta_data_path, "w") as file:
        json.dump(meta_data, file)

