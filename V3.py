import pandas as pd
import numpy as np
import csv
from decimal import Decimal, ROUND_UP

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

def pointsOnly(points,scorer):
    for player in floor:
        if player.id == scorer:
            team = player.team
            break

    for player in floor:
        if player.team == team:
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
answer = open("try.csv", "w")
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

freeThrowHold = [3,4,7,8,9,11,14,15,18,20]

actionPlays = [1,2,3,5,12,13]

# This is a boolean variable, which will be used in the occasional case when on a rebound play, we are not told who has secured the rebound. When this happens, whatever the team is of the next play following, that is the team that secured the previous plays rebound. So when this is set to "True", we will verify the team. It must originally be set to "false".
needToCheck = False

# This is a boolean variable which will be used when a foul is committed and there is a possible free throw situation. This will freeze substitutions for the time, so correct stats can be recorded. The list will hold the substitutions that must be made after the final free throws are complete.
subFreeze = False
heldSubs = []

heatCheck = False
extraPoss = False
playClock = None
foulClock = None
stop = False
time = False
teamTimeout = None
offenseReboundingTeam = None
reboundTime = None
follow = False
turnoverClock = None
turnover = False

# This is the main outer loop grouping all the plays by game.
for game,group in playFile.groupby("Game_id"):
# Sort the game on the basis of the world clock time first, and then on event number. This gives the true ordering for the game.
    sortedGameData = group.sort_values(by=["Period","PC_Time","WC_Time","Event_Num"], ascending=[True,False,True,True])

    sortedGameData = sortedGameData.reset_index(drop=True)

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

        if reboundTime != play["PC_Time"] and follow:
            follow = False

        if turnoverClock != play["PC_Time"] and turnover:
            turnover = False

        if time:
            if play["PC_Time"] != reboundTime:
                time = False


# This statement will only execute in the case that "subFreeze" has been set to true, meaning that in one of the most recent plays, there has been a foul called. If this has happened, but the current play is not a free throw, "3", or a substitution, "8", then the freeze is unnecessary, since there is no reason to put off the substitution. So we make the freeze equal to false, and execute any substitutions that were saved in the "heldSubs" list.
        #if subFreeze and play["Event_Msg_Type"] not in freeThrowHold:
        if foulClock != play["PC_Time"]:
            #subFreeze = False
            if heldSubs:
                for spot,bench in heldSubs:
                    floor[spot] = bench
                del heldSubs[:]

# If the Event_Msg_Type is equal to "12", and the period is greater than "1", then this is the start of a period that is not the start of a game. Here we must just change the floor lineup in case of a substitution during th quarter break.
        if play["Event_Msg_Type"] == 12 and play["Period"] > 1:
# Exact same logic as above when we filled the floor list at the beginning of a game.
            GameLineNewQuarter = lineup.get_group((game, play["Period"]))
            floor = [athlete for athlete in roster if any(athlete.id == starter["Person_id"] for index,starter in GameLineNewQuarter.iterrows())]

# If the Event_Msg_Type is a "1", then it's a made shot, which is the end of a possession. For every player on the floor, depending on their team, call the function to add to their offensive or defensive stats.
        elif play["Event_Msg_Type"] == 1:
            pointsAndPossession(play["Option1"])
            shotTime = play["PC_Time"]
            playClock = play["PC_Time"]

# If the short has been missed, we set the variable "play["Team_id"]" to the team that took the shot. Since every missed shot is followed by a rebound, we must check on the rebound play if it was an offensive or defensive rebound.
        elif play["Event_Msg_Type"] == 2:
            reboundTime = sortedGameData.loc[index+1]["PC_Time"]

            rebounder = None
            for candidate in floor:
                if candidate.id == sortedGameData.loc[index+1]["Person1"]:
                    rebounder = candidate
                    break

            if rebounder is None:
                if sortedGameData.loc[index+2]["Team_id"] != play["Team_id"]:
                    offenseReboundingTeam = False
                    #foulClock = sortedGameData.loc[index+1]["PC_Time"]
                    possessionOnly(play["Team_id"])
                else:
                    offenseReboundingTeam = True

# If the team of the rebounder is different then "play["Team_id"]", then the opposing team to the shooting team got the rebound. This results in a possession change, but since no points were scored, we only add the appropriate offensive or defensive possessions to the players on the floor. If the rebounder's team is the same as "play["Team_id"]", then this was an offensive rebound, so we can ignore it since no possession changes, and no points were scored.
            elif rebounder.team != play["Team_id"]:
                offenseReboundingTeam = False
                #foulClock = sortedGameData.loc[index+1]["PC_Time"]
                possessionOnly(play["Team_id"])
                if heldSubs:
                    for spot, bench in heldSubs:
                        if bench.team == play["Team_id"]:
                            bench.offPos -= 1
                        else:
                            bench.defPos -= 1

            else:
                offenseReboundingTeam = True

# An Event_Msg_Type of "3" is a free throw which has a few different types.
        elif play["Event_Msg_Type"] == 3:
# Stand alone special case: If Action_Type is "10", and the Option1 is "1", then this was a made "and one" free throw, so we add the stats to the players on the court, but we do not add a possession since it was already added on the made shot since this is an "and one". We also set "subFreeze" to false, since it may be true at this time, but now since the final free throw of the possession has been made, the new players can come onto the floor now
            if play["Action_Type"] == 10:
                #stop = False
                if play["Option1"] == 1:
                    pointsAndPossession(play["Option1"])
                    playClock = play["PC_Time"]
                else:
                    #subFreeze = False
                    if heldSubs:
                        for spot,bench in heldSubs:
                            if floor[spot].team == play["Team_id"]:
                                floor[spot].offPos += 1
                            else:
                                floor[spot].defPos += 1
                            floor[spot] = bench
                        del heldSubs[:]


                    rebounder = None
                    for candidate in roster:
                        if candidate.id == sortedGameData.loc[index+1]["Person1"]:
                            rebounder = candidate
                            follow = True
                            for check in floor:
                                if rebounder == check:
                                    follow = False
                                    break
                            break

                    if rebounder is None:
                        if sortedGameData.loc[index+2]["Team_id"] != play["Team_id"]:
                            offenseReboundingTeam = False
                            possessionOnly(play["Team_id"])
                        else:
                            offenseReboundingTeam = True


                    elif rebounder.team != play["Team_id"]:
                        offenseReboundingTeam = False
                        possessionOnly(play["Team_id"])

                    else:
                        offenseReboundingTeam = True

# This group will only add points and no possessions since no possession change is possible when there are no rebounds. We must put the "if play["Option1"]" statement inside of the outer if statement because if the free throw is missed, nothing happens to any players points or possessions. If it was on the outside condition, like on the free throws with rebounds in the next "elif", then execution would fall to the "else" statement at the end, and would unnecessarily keep track of the team who shot the free throw.
            elif play["Action_Type"] in freeThrowActionsNoRebound:
                if play["Option1"] == 1:
                    pointsOnly(play["Option1"] , play["Person1"] )
# This group will add points and possessions if the free throw is made, since rebounds were possible.
            elif play["Action_Type"] in freeThrowActionsRebound and play["Option1"] == 1:
                #stop = False
                playClock = play["PC_Time"]
                pointsAndPossession(play["Option1"])
                if heldSubs:
                    for spot, bench in heldSubs:
                        if floor[spot].team == play["Team_id"]:
                            floor[spot].offPos -= 1
                        else:
                            floor[spot].defPos -= 1

# If all other cases are false, then the only possible thing that could have happened was a missed free throw, that had a possible rebound. If this is the case, we must set the "play["Team_id"]" variable to the free throw shooting team, and look to the next play which will be a rebound.
            else:
                reboundTime = sortedGameData.loc[index+1]["PC_Time"]
                teamShot = play["Team_id"]

                if heldSubs:
                    for spot,bench in heldSubs:
                        floor[spot] = bench
                    del heldSubs[:]

                rebounder = None
                for candidate in roster:
                    if candidate.id == sortedGameData.loc[index+1]["Person1"]:
                        rebounder = candidate
                        follow = True
                        for check in floor:
                            if check == rebounder:
                                follow = False
                                break

                if rebounder is None:
                    if sortedGameData.loc[index+2]["Team_id"] != play["Team_id"]:
                        offenseReboundingTeam = False
                        possessionOnly(play["Team_id"])
                        if heldSubs:
                            for spot, bench in heldSubs:
                                if floor[spot].team == play["Team_id"]:
                                    floor[spot].offPos -= 1
                                else:
                                    floor[spot].defPos -= 1
                    else:
                        offenseReboundingTeam = True

                elif rebounder.team != play["Team_id"]:
                    offenseReboundingTeam = False
                    possessionOnly(play["Team_id"])
                    if heldSubs:
                        for spot, bench in heldSubs:
                            if bench.team == play["Team_id"]:
                                bench.offPos -= 1
                            else:
                                bench.defPos -= 1
                else:
                    offenseReboundingTeam = True

# If the Event_Msg_Type is a "5", this is a turnover. Therefore, we just add the appropriate possessions to the players on the floor, and no points. Offensive possessions are given to the team that committed the turnover.
        elif play["Event_Msg_Type"] == 5:
            teamTurnover = play["Team_id"]
            possessionOnly(play["Team_id"])
            turnoverClock = play["PC_Time"]

# If a foul is committed on a play,then we must freeze all substitutions for the time being. If any substitutions are made during free throws, then we must wait until after the free throws go through to before making the substitutions.
        elif play["Event_Msg_Type"] == 6:
            #subFreeze = True
            foulClock = play["PC_Time"]
            if shotTime == play["PC_Time"]:
                #stop = True
                #print(play["Event_Num"])
                for player in floor:
                    if player.team == sortedGameData.loc[index-1]["Team_id"]:
                        player.offPos -= 1
                    else:
                        player.defPos -= 1
            if play["PC_Time"] == turnoverClock and teamTurnover != play["Team_id"]:
                turnover = True


# If the Event_Msg_Type is an "8", this is a substitution. Person1 is leaving the game, Person2 is entering the game.
        elif play["Event_Msg_Type"] == 8:
# First we need to check all players on the floor to figure out the index of who needs to be subbed out in the floor list. After the spot is found, then we go through the roster and find the person who is being subbed in from the bench and insert that player into the index of the sub.

            for sub in floor:
                if sub.id == play["Person1"]:
                    spot = floor.index(sub)
                    if playClock != play["PC_Time"] and shotTime != play["PC_Time"] and turnoverClock != play["PC_Time"] and not time:
                        #print(play["Event_Num"])
                        if sub.team == play["Team_id"]:
                            sub.offPos += 1
                        else:
                            sub.defPos += 1
                    elif turnover:
                        if sub.team == teamTurnover:
                            sub.defPos += 1
                        else:
                            sub.offPos += 1
                    """
                    elif turnoverClock == foulClock and turnoverClock == play["PC_Time"] and foulClock == play["PC_Time"] and sortedGameData.loc[index-1]["Event_Msg_Type"] != 5:
                        if play["Event_Num"] == 482 and game == "096e231adad0be6ab1cc89cce56847f8":
                            print("yeeete")
                        if sub.team == play["Team_id"]:
                            sub.offPos += 1
                        else:
                            sub.defPos += 1
                    """

                    """
                    elif subFreeze == True and foulClock == play["PC_Time"]:
                        if sub.team == play["Team_id"]:
                            sub.offPos += 1
                        else:
                            sub.defPos += 1
                    """
                    for bench in roster:
                        if bench.id == play["Person2"]:

                            if reboundTime == play["PC_Time"] and follow:
                                if bench.team == teamShot:
                                    bench.offPos += 1
                                else:
                                    bench.defPos += 1

                            if foulClock == play["PC_Time"]:
                                heldSubs.append([spot,bench])
                            else:
                                floor[spot] = bench
                            break
                    break

        elif play["Event_Msg_Type"] == 9:
            #teamTimeout = play["Team_id"]
            if play["PC_Time"] == reboundTime:
                time = True
                if offenseReboundingTeam:
                    time = False


        elif play["Event_Msg_Type"] == 13:
            possessionOnly(play["Team_id"])


        elif play["Event_Msg_Type"] == 16:
            for player in roster:
                if player.offPos == 0 and player.defPos == 0:
                    output.writerow([play["Game_id"], player.id, "N/A", "N/A"])

                else:
                    if player.id == "7a1c1f680a11456d505f05fa70712213" :
                        print(100 *(player.pointsAgainst/player.defPos))
                        check = Decimal(str(100 *(player.pointsAgainst/player.defPos))).quantize(Decimal('.1'), rounding=ROUND_UP)
                        print(check)
                    output.writerow([play["Game_id"], player.id, round(100 *(player.pointsFor/player.offPos),1), round(100 *(player.pointsAgainst/player.defPos),1)])

            del roster[:], floor[:]

        if play["Event_Num"] == 581 and game == "117a5a71c34c2d8a39ff66d884462bd7":


            print(roster[3].id)
            print(roster[3].team)
            print(roster[3].pointsFor)
            print(roster[3].offPos)
            print(roster[3].pointsAgainst)
            print(roster[3].defPos)


            #exit(0)


        #elif play["Event_Msg_Type"] == 12 or play["Event_Msg_Type"] == 10 or play["Event_Msg_Type"] == 7 or play["Event_Msg_Type"] == 9 or play["Event_Msg_Type"] == 20 or play["Event_Msg_Type"] == 18 or play["Event_Msg_Type"] == 13:
            #continue

        else:
            continue
            #subFreeze = True
            #print(play)
            #exit(0)
