import os

from authentication import authentication
from elections import create
from elections import view
from elections import participate

# Declaration section
creds = None
user_email = None


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def start_app():
    """
    This function handles the entry of the application. Giving the user the option to login
    """
    global creds, user_email
    while True:
        print("""Welcome to Voting Application!
        Select an option to continue (e.g. 1)
        [1] Log in to Voting App
        [2] Exit""")
        userinput = input("Option: ")
        if userinput == "1":
            clear_screen()
            print("Trying to log in...")
            print()
            creds = authentication.authenticate()
            user_email = authentication.get_user_data(creds)
            print()
            break
        elif userinput == "2":
            clear_screen()
            print("Logging out...")
            print()
            exit()
        else:
            clear_screen()
            print("Invalid input try again")
            print()


def prompt_for_action():
    """
    This function handles the main menu of the voting application. It displays a list of options
    for the user to choose from and performs the corresponding action based on the user's input.
    """
    while True:
        print("""Select an option to continue
        [1] View Elections
        [2] Create an Election
        [3] Participate in an Election
        [4] Exit""")
        userinput = input("Option: ")
        if userinput == "1":
            clear_screen()
            print("Viewing Elections...")
            print()
            show_elections_view()
        elif userinput == "2":
            clear_screen()
            print("Creating Election...")
            print()
            prompt_for_election_data()
        elif  userinput == "3":
            clear_screen()
            print("Participating in Election...")
            print()
            prompt_for_vote()
        elif userinput == "4":
            clear_screen()
            print("Logging out...")
            print()
            exit()
        else:
            clear_screen()
            print("Invalid input try again")
            print()


def prompt_for_election_data():
    """
    Prompts the user to input data for creating a new election.
    Collects the title, number of options, details of each option,
    self-voting permission, public election status, and allowed voters.
    Calls the create_election function from the 'create' module to create the election.
    """
    global user_email

    title = create.get_election_title()
    options_number = create.get_options_number()
    options_and_data = create.get_options_details(options_number)
    allow_self_voting = create.get_is_self_voting()
    is_public_election = create.get_is_public_election()
    allowed_voters = create.get_allowed_voters(is_public_election)

    create.create_election(title,
                             options_and_data,
                             allow_self_voting,
                             is_public_election,
                             user_email,
                             allowed_voters)
    
    print("Election successfully created!")
    print()


def show_elections_view():
    """
    Displays the list of available elections and allows the user to view the details of a chosen election.
    """
    global user_email

    elections = view.get_elections()
    if len(elections) == 0:
        print("There are no polls / elections available at this time!")
        print()
        return
    chosen_election = view.get_chosen_election(elections)
    
    clear_screen()
    
    if not view.is_allowed_to_view(user_email, chosen_election):
        return
    
    election_data = view.read_meta_data(chosen_election)
    view.print_election_title(election_data)
    view.print_is_self_voting(election_data)
    view.print_is_public_election(election_data)
    view.print_election_creator(election_data)
    view.print_voters(election_data)
    view.print_votes(election_data)

    print()


def prompt_for_vote():
    """
    Prompts the user to vote in a chosen election.
    """
    global user_email
    elections = view.get_elections()
    if len(elections) == 0:
        return
    
    # name of election (not number)
    chosen_election = view.get_chosen_election(elections)
    
    clear_screen()

    if not participate.is_allowed_to_vote(user_email, chosen_election):
        return
    
    candidates = participate.get_candidates(chosen_election)
    chosen_candidate_number = participate.prompt_for_option(candidates)
    option_chosen = candidates[chosen_candidate_number-1][0]
    
    participate.write_vote(chosen_election, user_email, option_chosen)
    participate.update_vote_score(chosen_election, option_chosen)
    
    clear_screen()
    print("Voted Successfully!")
    print()


# main function
def main ():
    clear_screen()
    start_app()
    prompt_for_action()


if "__main__" == __name__:
    main()
