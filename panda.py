import pandas as pd
import numpy as np
import csv

class Player:
    def __init__(self, team, id):
        self.team = team
        self.id = id
        self.pointsFor = 0
        self.pointsAgainst = 0
        self.offPos = 0
        self.defPos = 0

    def offensiveEnd(self, points):
        self.pointsFor += points
        self.offPos += 1

    def defensiveEnd(self, points):
        self.pointsAgainst += points
        self.defPos += 1

    def offensivePoint(self, points):
        self.pointsFor += points

    def defensivePoint(self, points):
        self.pointsAgainst += points

# Creates a new .csv file and puts it in csv writer mode.
answer = open("answer.csv", "w")
output = csv.writer(answer)

# Writes the column headers in the answer file in .csv format
answerHeaders = ["Game_ID", "Player_ID", "OffRtg", "DefRtg"]
output.writerow(answerHeaders)

# Opens the file with all the plays, and turns it into a data frame using pandas.
playFile = pd.read_csv("plays.txt", delimiter="\t")

# Opens the file with the lineups, and turns it into a data frame using pandas. We then group the data based on their Game_id, and the period.
lineupFile = pd.read_csv("Game_Lineup.txt", delimiter="\t")
lineup = lineupFile.groupby(["Game_id","Period"])

# These are the two lists needed to keep track of the roster of everyone in the game, as well as everyone on the floor.
roster = []
floor = []

# This is the main outer loop grouping all the plays by game.
for game,group in playFile.groupby("Game_id"):
# Sort the game on the basis of the world clock time first, and then on event number. This gives the true ordering for the game.
    sortedGameData = group.sort_values(by=["WC_Time","Event_Num"])


# MAYBE HAVE TO DELETE HERE, MAYBE HAVE TO DELETE WHEN PUTTING THE DATA INTO THE OUTPUT FILE.

    del roster[:], floor[:]
# Whenever a new game begins, we must fill the roster list, as well as the floor list. To do this, we go into the lineup data and get the group that has the correct Game_id, and has a period of zero.
    GameLineBeginning = lineup.get_group((game,0))
# This step uses a list comprehension to create a new object for every player at the start of a game, and creates a roster list. So it takes the Team_id and the Person_id from every row in the game's data frame, and makes the structure and the list.
    roster = [Player(player["Team_id"],player["Person_id"]) for index,player in GameLineBeginning.iterrows()]
# We then have to fill the floor list. To do that, we look in the lineup data again, and get the group of the same game, but with period of one.
    GameLineQuarter1 = lineup.get_group((game, 1))
# Using list comprehsion again, we add every athlete from the roster list, only if they're on the floor at the beginning of the game, making them a starter.
    floor = [athlete for athlete in roster if any(athlete.id == starter["Person_id"] for index,starter in GameLineQuarter1.iterrows())]


# Now that the roster and floor lists are filled, we go through each play of the game.
    for index,play in sortedGameData.iterrows():
# If the Event_Msg_Type is equal to "12", and the period is greater than "1", then this is the start of a period that is not the start of a game. Here we must just change the floor lineup in case of a substitution during th quarter break.
        if play["Event_Msg_Type"] == 12 and play["Period"] > 1:
# Exact same logic as above when we filled the floor list at the beginning of a game.
            GameLineNewQuarter = lineup.get_group((game, play["Period"]))
            floor = [athlete for athlete in roster if any(athlete.id == starter["Person_id"] for index,starter in GameLineNewQuarter.iterrows())]
            exit(0)

        elif play["Event_Msg_Type"] == 1:
            for player in floor:
                if player.team == play["Team_id"]:
                    player.offensiveEnd(play["Option1"])
                else:
                    player.defensiveEnd(play["Option1"])
            print("\n")
            print("Floor:")
            print("\n")
            for z in floor:
                print(z.id)
                print(z.team)
                print(z.pointsFor)
                print(z.pointsAgainst)
                print("\n")
            exit(0)

        elif play["Event_Msg_Type"] == 12 or play["Event_Msg_Type"] == 10:
            continue

        else:
            print(play)
            exit(0)
