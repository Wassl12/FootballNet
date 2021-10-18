## Steps to run
1. Run data.py (from data/)
1. Run preprocessing.py (from data/)
   1. A prelim roster is a roster made of recruits we speculate are still on the team
   1. A verified roster is the correct roster
   1. Finalized roster is the intersection of 2a and 2b
1. Run team.py
1. Run databuilder.py
1. Run predict.py
## data.py
Data is stored in JSONs. Please try to minimize calls to the API... (Use data.py to make API calls and do so sparingly).
Always download a JSON if you access it from the API.

## preprocessing.py
This script combines raw recruiting data with team rosters to develop a "finalized" roster that is a set intersection of recruits and the current roster.

## team.py
Organizes the data into large tensors per team. Team data (especially recruiting data) is duplicated many times throughout the script, so this attaches arrays to dictionaries.
It's highly important that you fit this script to your architecture. Data needs to be formatted for the model, so pay attention to tensor size, what variables are inserted into team
tensors, etc.

## databuilder.py
Accesses the dictionary of arrays from the prior script. Copies a team's corresponding tensor and stacks it onto the opponent's tensor. This tensor will be what the model trains on.
Jumbles home and away teams so that the model doesn't take shortcuts. Ensure that home teams and away teams appear on random halves of the "game" tensor or the model learns shortcuts.

## predict.py
Runs the pytorch training algorithm. Doesn't use a data loader because the dataset is small. Adjust batch size to fit your needs and make changes to dataloading depending on tensor size.
