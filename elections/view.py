import os
import json

# Declaration section
current_directory = os.getcwd()
subdirectory_path = os.path.join(current_directory, "database")


def get_elections():
    elections = sorted(os.listdir(subdirectory_path))
    for election in elections:
        print(election)
    return elections


def get_chosen_election(elections):
    while True:
        election_number = input("Enter the poll / election number: ")
        try:
            election_number = int(election_number)
            election = elections[election_number-1]
            return election
        except:
            continue


def read_meta_data(chosen_election):
    meta_data = os.path.join(subdirectory_path, chosen_election, "metadata.json")
    with open(meta_data, 'r') as file:
        data = json.load(file)
    return data


def is_allowed_to_view(user_email, chosen_election):
    meta_data = read_meta_data(chosen_election)
    
    if user_email == meta_data["creator"]:
        return True
    elif meta_data["voters"] == ["everyone"]:
        return True
    
    return False


def print_election_title(chosen_election):
    print()
    title = chosen_election["title"]
    print(f"The title of this election is: {title}")
    print()


def print_votes(chosen_election):
    total_votes = 0
    for option, votes in chosen_election["election_data"].items():
        print(f"{option.capitalize()} has {votes} vote(s).")
        total_votes += votes
    print(f"Total votes for this election: {total_votes}")
    print()


def print_is_self_voting(chosen_election):
    selfvoting = chosen_election["self_voting"]
    print(f"Is the maker of the election allowed to vote?: {selfvoting}")
    print()


def print_is_public_election(chosen_election):
    is_public = chosen_election["public_election"]
    print(f"Is this a public election: {is_public}")
    print()


def print_election_creator(chosen_election):
    creator = chosen_election["creator"]
    print(f"The creator of this election is: {creator}")
    print()


def print_voters(chosen_election):
    voters = chosen_election["voters"]
    print(f"People allowed to vote in: {voters}")
    print()
    