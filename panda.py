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

    def offensivePointsAndPossession(self, points):
        self.pointsFor += points
        self.offPos += 1

    def defensivePointsAndPossession(self, points):
        self.pointsAgainst += points
        self.defPos += 1

    def offensivePoints(self, points):
        self.pointsFor += points

    def defensivePoints(self, points):
        self.pointsAgainst += points

    def offensivePossession(self):
        self.offPos += 1

    def defensivePossession(self):
        self.defPos += 1


def pointsAndPossession(points):
    for player in floor:
        if player.team == play["Team_id"]:
            player.offensivePointsAndPossession(points)
        else:
            player.defensivePointsAndPossession(points)

def pointsOnly(points):
    for player in floor:
        if player.team == play["Team_id"]:
            player.offensivePoints(points)
        else:
            player.defensivePoints(points)

def possessionOnly(offensiveTeam):
    for player in floor:
        if player.team == offensiveTeam:
            player.offensivePossession()
        else:
            player.defensivePossession()


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

# These two lists will be used in the case of free throws. There are many different types of free throws, but we can split all but one of them into two distinct groups. The separator being whether they are reboundable or not.
freeThrowActionsNoRebound = [11,13,14,16,17,18,19,20,21,22,25,26,27,28,29]
freeThrowActionsRebound = [12,15]

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

# If the Event_Msg_Type is a "1", then it's a made shot, which is the end of a possession. For every player on the floor, depending on their team, call the function to add to their offensive or defensive stats.
        elif play["Event_Msg_Type"] == 1:
            #continue
            pointsAndPossession(play["Option1"])

# If the short has been missed, we set the variable "teamShot" to the team that took the shot. Since every missed shot is followed by a rebound, we must check on the rebound play if it was an offensive or defensive rebound.
        elif play["Event_Msg_Type"] == 2:
            teamShot = play["Team_id"]

# An Event_Msg_Type of "3" is a free throw which has a few different types.
        elif play["Event_Msg_Type"] == 3:
# Stand alone special case: If Action_Type is "10", and the Option1 is "1", then this was a made "and one" free throw, so we add the stats to the players on the court, but we do not add a possession since it was already added on the made shot since this is an "and one".
            if play["Action_Type"] == 10 and play["Option1"] == 1:
                pointsOnly(play["Option1"])
# This group will only add points and no possessions since no possession change is possible when there are no rebounds. We must put the "if play["Option1"]" statement inside of the outer if statement because if the free throw is missed, nothing happens to any players points or possessions. If it was on the outside condition, like on the free throws with rebounds in the next "elif", then execution would fall to the "else" statement at the end, and would unnecessarily keep track of the team who shot the free throw.
            elif play["Action_Type"] in freeThrowActionsNoRebound:
                if play["Option1"] == 1:
                    pointsOnly(play["Option1"])
# This group will add points and possessions if the free throw is made, since rebounds were possible.
            elif play["Action_Type"] in freeThrowActionsRebound and play["Option1"] == 1:
                pointsAndPossession(play["Option1"])
# If all other cases are false, then the only possible thing that could have happened was a missed free throw, that had a possible rebound. If this is the case, we must set the "teamShot" variable to the free throw shooting team, and look to the next play which will be a rebound.
            else:
                teamShot = play["Team_id"]

# This is a rebound, so we must check the teamShot variable to see who shot the last shot, and compare it to the team of the player who rebounded the ball.
        elif play["Event_Msg_Type"] == 4:
# Create a variable called rebounder, which will store the value of the player who rebounded the prior missed shot. We go through all players on the floor to find this player.
            rebounder = None
            for candidate in floor:
                if candidate.id == play["Person1"]:
                    rebounder = candidate
                    break
# After the loop completes, if rebounder is still "None", then this is the case of a team rebound, which must be handled separately.
            if rebounder is None:
                print(teamShot)
                exit(0)
# If the team of the rebounder is different then "teamShot", then the opposing team to the shooting team got the rebound. This results in a possession change, but since no points were scored, we only add the appropriate offensive or defensive possessions to the players on the floor. If the rebounder's team is the same as "teamShot", then this was an offensive rebound, so we can ignore it since no possession changes, and no points were scored.
            elif rebounder.team != teamShot:
                possessionOnly(teamShot)

# If the Event_Msg_Type is a "5", this is a turnover. Therefore, we just add the appropriate possessions to the players on the floor, and no points. Offensive possessions are given to the team that committed the turnover.
        elif play["Event_Msg_Type"] == 5:
            possessionOnly(play["Team_id"])

        elif play["Event_Msg_Type"] == 12 or play["Event_Msg_Type"] == 10 or play["Event_Msg_Type"] == 6:
            continue

        else:
            print(play)
            exit(0)
