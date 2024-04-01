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
    meta_data = os.path.join(voter_data_path, chosen_election, "option_data.json")
    with open(meta_data, 'r') as file:
        data = json.load(file)
    return data


def get_candidates(chosen_election):
    candidate_data = read_candidate_data(chosen_election)

    candidates = []
    for option, additional_infromation in candidate_data.items():
        candidates.append([option, additional_infromation])
    
    return candidates


def prompt_for_option(candidate_list):
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
    voter_file = os.path.join(voter_data_path, chosen_election, 'voter_data.txt')

    encrypted_email = encryption.encrypt_email(email)
    with open(voter_file, "ab") as file:
        file.write(encrypted_email + b'\n')


def get_secret_email(email):
    return encryption.encrypt_email(email)


def update_vote_score(chosen_election, option ):
    meta_data = view.read_meta_data(chosen_election)

    meta_data["election_data"][option] += 1

    meta_data_path = os.path.join(voter_data_path, chosen_election, "metadata.json")
    with open(meta_data_path, "w") as file:
        json.dump(meta_data, file)

