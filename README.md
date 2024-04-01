
# Account Requirements:
- A Google email

---

# System Requirements:
- An internet connection
- A linux based machine
- Bash terminal
- Python3
- Pip

---

# Running instructions:
- Open terminal in the application's directory
- Run this command in terminal --> pip install -r dependencies requirements.txt
    (installs the dependencies)
- Run this command in terminal --> python3 project.py

---

# Testing instructions:
- Run this command in terminal --> python3 test_project.py

---

# Summary:
<p>
A polling app that can be used to host polls / elections to gather data. Creating a poll involoves:
 naming the poll / election, providing the number of options/candidates, entering information about each candidate, answering whether the creator of the poll is also allowed to vote and whether it is a public election or not. For non-public polls/elections only specified people are allowed to vote.

 Viewing polls / elections involoves prompting the user prompting the user for an input. The user then enters the poll number for the poll they want view. If there are no polls the user is returned to the previous screen. If the poll is public any user can view the details of the poll. If the poll is private only the owner is allowed to view the details of the poll. Details shown about the poll include: the title, whether the is allowed to vote, whether it is a public poll, the poll creator, the votes for each option / candidate, the total votes in the poll.

 Participating in a poll / election involves showing the user available polls. Then prompting the user for the poll they wish to participate in. If there are no polls the user is returned to the previous screen. Based on the chosen poll checks are made whether the user is allowed to vote in this poll (the poll may be private). If the user is not allowed to vote they are returned to the previous screen. If they are allowed to vote then the options / candidates are printed and the user is prompted for their choice. Once chosen the voting data is written and the scored are updated automatically.
</p>

---

# Key Features:
- Using Google Oauth to login and authenticate users
- Using Fernet to mask voter emails
