import pandas as pd
import csv
import math

# This is the player object used to track every player's statistics.
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

# The following three functions are helper functions to add points and/or possesions to the appropriate players and teams.
def pointsAndPossession(points):
    for player in floor:
        if player.team == play["Team_id"]:
            player.offensivePointsAndPossession(points)
        else:
            player.defensivePointsAndPossession(points)

def pointsOnly(points,scorer):
    for player in roster:
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
answer = open("Team_Vancouver_Q1_BBALL.csv", "w")
output = csv.writer(answer)

# Writes the column headers in the answer file in .csv format
answerHeaders = ["Game_ID", "Player_ID", "OffRtg", "DefRtg"]
output.writerow(answerHeaders)

# Opens the file with all the plays, and turns it into a data frame using pandas.
playFile = pd.read_csv("Play_by_Play.txt", delimiter="\t")

# Opens the file with the lineups, and turns it into a data frame using pandas. We then group the data based on their Game_id, and the period.
lineupFile = pd.read_csv("Game_Lineup.txt", delimiter="\t")
lineup = lineupFile.groupby(["Game_id","Period"])

# These are the two lists needed to keep track of the roster of everyone in the game, as well as everyone on the floor.
roster = []
floor = []

# These two lists will be used in the case of free throws. There are many different types of free throws, but we can split all but one of them into two distinct groups. The separator being whether they are reboundable or not.
freeThrowActionsNoRebound = [11,13,14,16,17,18,19,20,21,22,25,26,27,28,29]
freeThrowActionsRebound = [12,15]

# This is the list that will hold the substitutions that must wait to be prcoessed until the previous play is over such as during freethrows.
heldSubs = []

# Multiple Boolean variables that are used throughout the program. These will be explained in detail as they appear.
playClock = None
foulClock = None
time = False
offenseReboundingTeam = None
reboundTime = None
follow = False
turnoverClock = None
turnover = False

# This is the main outer loop grouping all the plays by game.
for game,group in playFile.groupby("Game_id"):
# Sort the game's how they were outlined in the instructions based on Period, times and event numbers.
    sortedGameData = group.sort_values(by=["Period","PC_Time","WC_Time","Event_Num"], ascending=[True,False,True,True])
# Once the game data is sorted correctly, this step resets the indexes of the plays so that the new order created is in numerically ascending order by index number. Since the original index numbers were assigned to the original order of the file, many of the indexes would have been shifted after the organization in the previous step, making this step necessary.
    sortedGameData = sortedGameData.reset_index(drop=True)
# Whenever a new game begins, we must fill the roster list, as well as the floor list. To do this, we go into the lineup data and get the group that has the correct Game_id, and has a period of zero.
    GameLineBeginning = lineup.get_group((game,0))
# This step uses a list comprehension to create a new object for every player at the start of a game, and creates a roster list. It takes the Team_id and the Person_id from every row in the game's data frame, makes the data structure and creates the list.
    roster = [Player(player["Team_id"],player["Person_id"]) for index,player in GameLineBeginning.iterrows()]
# We then have to fill the floor list. To do that, we look in the lineup data again, and get the group of the same game, but with period of one.
    GameLineQuarter1 = lineup.get_group((game, 1))
# Using list comprehsion again, we add every athlete from the roster list, only if they're on the floor at the beginning of the game, making them a starter.
    floor = [athlete for athlete in roster if any(athlete.id == starter["Person_id"] for index,starter in GameLineQuarter1.iterrows())]

# Now that the roster and floor lists are filled, we go through each play of the game.
    for index,play in sortedGameData.iterrows():

# These three initial checks have to do with situations involving rebounds, turnovers and timeouts. The nature of these variables will be explained later.
        if reboundTime != play["PC_Time"] and follow:
            follow = False

        if turnoverClock != play["PC_Time"] and turnover:
            turnover = False

        if time:
            if play["PC_Time"] != reboundTime:
                time = False

# This statement executes only when the variable "foulClock" no longer is equal to the current plays time. The variable "foulClock" gets assigned the current game time when a foul occurs. For each of the plays following, if those play's game times are still equal to the foul time, we must hold off on executing substitutions, since it is possible that free throws are being taken. If free throws are following, then the possession has not ended, and the subs are not considered on the floor yet. Once the current play's time no longer equals the time of the last foul, then we can execute any substitutions that were saved in the "heldSubs" list.
        if foulClock != play["PC_Time"]:
            if heldSubs:
                for spot,bench in heldSubs:
                    floor[spot] = bench
                del heldSubs[:]

# If the Event_Msg_Type is equal to "12", and the period is greater than "1", then this is the start of a period that is not the start of a game. Here we must just change the floor lineup in case of a substitution during th quarter break.
        if play["Event_Msg_Type"] == 12 and play["Period"] > 1:
# Exact same logic as above when we filled the floor list at the beginning of a game.
            GameLineNewQuarter = lineup.get_group((game, play["Period"]))
            floor = [athlete for athlete in roster if any(athlete.id == starter["Person_id"] for index,starter in GameLineNewQuarter.iterrows())]

# If the Event_Msg_Type is a "1", then it's a made shot, which is the end of a possession. For every player on the floor, depending on their team, we add to their appropriate stats. We also set the variables "shotTime" and "playClock" to the current time of the play. These variables are used in the case of a possible "and one" free throw occuring after this shot is scored, and accounts for possible substitutions. Both of these are explained later.
        elif play["Event_Msg_Type"] == 1:
            pointsAndPossession(play["Option1"])
            shotTime = play["PC_Time"]
            playClock = play["PC_Time"]

# If the short has been missed, then the Event_Msg_Type will be a "2". Every missed shot is followed immediately by a rebound, therefore instead of having two separate conditions for missed shots and rebounds, we will simply look a play ahead and deal with the rebound right away
        elif play["Event_Msg_Type"] == 2:
# We set the variable "reboundTime" to the following play's game time.
            reboundTime = sortedGameData.loc[index+1]["PC_Time"]
# Now we must go through and find the identity of the rebounder. We go through the full roster list and search for the rebounder. We must go through the entire roster, since there are cases in the play data in which the rebounder is not on the floor yet since the substitutions have been recorded after the rebound. So to account for this, we go through the entire roster, and if the rebounder is found in the roster, we then check if he is on the floor as well. If he is on the roster, but not on the floor, we set the variable "follow" to False, which is used in the substitution section, too account for this missing player. Otherwise, "follow" is left as true, and does not affect any substitutions
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
# If the rebounder is None at this point, that means that the rebounder was the "team", meaning the actual player was not recorded. So to find out which team this is, we must go ahead two plays, and check the "Team_id" of that play, since the team who rebounded the ball will be in control of the following play. If the team is different from the current play's team, then this was a defensive rebound, so we set the variable "offenseReboundingTeam" to False (explained later), and give everyone on the floor the appropriate possessions as the defensive rebound ended the previous possession. If the teams are the same, then we set offenseReboundingTeam to True, and do nothing else as the possession continues.
            if rebounder is None:
                if sortedGameData.loc[index+2]["Team_id"] != play["Team_id"]:
                    offenseReboundingTeam = False
                    possessionOnly(play["Team_id"])
                else:
                    offenseReboundingTeam = True

# If the rebounder is in the roster and team of the rebounder is different then "play["Team_id"]", then the opposing team to the shooting team got the rebound. This results in a possession change, but since no points were scored, we only add the appropriate offensive or defensive possession to the players on the floor, and once again set "offenseReboundingTeam" to False. If the rebounder's team is the same as "play["Team_id"]", then this was an offensive rebound, so we can ignore it since no possession changes, and set "offenseReboundingTeam" to True.
            elif rebounder.team != play["Team_id"]:
                offenseReboundingTeam = False
                possessionOnly(play["Team_id"])
            else:
                offenseReboundingTeam = True

# An Event_Msg_Type of "3" is a free throw which has a few different types.
        elif play["Event_Msg_Type"] == 3:
# If Action_Type is "10", then this is an "and". If Option1 is "1", then this was a made "and one" free throw, so we add the stats to the players on the court. We also set "playClock" to the current time, since it may be used later. If Option1 is not a "1", then this was a missed free throw.
            if play["Action_Type"] == 10:
                if play["Option1"] == 1:
                    pointsAndPossession(play["Option1"])
                    playClock = play["PC_Time"]
                else:
# In the case of a missed "and one" free throw, what we first must do is check the heldsubs list. If there are players waiting to be on the floor, the moment that the free throw is missed, they are now considered on the floor. So if the player's team is the same as the team that just missed the free throw, then they must be added an offensive possession, as they are now considered on the floor. The opposite is true if the player is on the opposing team, they must be added a defensive possession, and then can be put on the floor.
                    if heldSubs:
                        for spot,bench in heldSubs:
                            if floor[spot].team == play["Team_id"]:
                                floor[spot].offPos += 1
                            else:
                                floor[spot].defPos += 1
                            floor[spot] = bench
                        del heldSubs[:]
# This portion follows the same logic as the section above in handling the substitutions.
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

# This group will only add points and no possessions since no possession change is possible when there are no rebounds. If the free throw is missed, nothing happens to the play, so no "else" statement is needed
            elif play["Action_Type"] in freeThrowActionsNoRebound:
                if play["Option1"] == 1:
                    pointsOnly(play["Option1"] , play["Person1"] )
# This group will add points and possessions if the free throw is made, since rebounds were possible. The variable "playClock" is also set to the current time since later in subs this may be used.
            elif play["Action_Type"] in freeThrowActionsRebound and play["Option1"] == 1:
                playClock = play["PC_Time"]
                pointsAndPossession(play["Option1"])
# If there are subs being held at this point, then we need to subtract an offensive or defensive possession from each of the players exiting the floor. We must do this since we double count the player's on the floor possessions when they exit in this case.
                if heldSubs:
                    for spot, bench in heldSubs:
                        if floor[spot].team == play["Team_id"]:
                            floor[spot].offPos -= 1
                        else:
                            floor[spot].defPos -= 1

# If all other cases are false, then the only thing that could have happened was a missed free throw, that had a possible rebound. If this is the case, we must set the "reboundTime" variable to the time of the following play, since it will be a rebound. We also set the variable  "teamShot" to the free throw shooting team, which may be used later.
            else:
                reboundTime = sortedGameData.loc[index+1]["PC_Time"]
                teamShot = play["Team_id"]
# Same logic as above for the following section.
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

# If the Event_Msg_Type is a "5", this is a turnover. Therefore, we just add the appropriate possessions to the players on the floor, and no points. Offensive possessions are given to the team that committed the turnover. We also note the time that the turnover takes place, as well as the team that commited it.
        elif play["Event_Msg_Type"] == 5:
            teamTurnover = play["Team_id"]
            possessionOnly(play["Team_id"])
            turnoverClock = play["PC_Time"]

# If a foul is committed on a play,then we must freeze all substitutions for the time being. If any substitutions are made during free throws, then we must wait until after the free throws go through to before making the substitutions. To do this, we set the variable "foulClock" to the time of the foul, which will be compared to for the following plays
        elif play["Event_Msg_Type"] == 6:
            foulClock = play["PC_Time"]
# If the variable "shotTime" is the same as the time of the foul, then this is the case of a foul that happened immediately after a scored shot, making this an "and one" foul. Since both possessions and points were added on the made shot attempt in a previous play, we must now remove a possession for every player on the floor, because the foul will need a free throw, making the previous possession not finished.
            if shotTime == play["PC_Time"]:
                for player in floor:
                    if player.team == sortedGameData.loc[index-1]["Team_id"]:
                        player.offPos -= 1
                    else:
                        player.defPos -= 1
# If the time of the foul is the same as the last turnover, and the team that committed the turnover is different from the team of the foul, then we set the variable "turnover" to be True, because if a substitution is followed immediately after these events, we must add possessions to the players involved in the sub.
            if play["PC_Time"] == turnoverClock and teamTurnover != play["Team_id"]:
                turnover = True

# If the Event_Msg_Type is an "8", this is a substitution. Person1 is leaving the game, Person2 is entering the game.
        elif play["Event_Msg_Type"] == 8:
# First we need to check all players on the floor to figure out the index of who needs to be subbed out in the floor list. After the spot is found, we then go through three conditions. The goal of the three conditions is to make sure that this substitution needs to add a possession to the player who is leaving the game. If "playClock" is equal to the current time of the play, then we do not need to add a possession, since the possession has already been added. If "turnoverClock" is equal to the current time of the play, then the possession from the turnover has already been added, and we do not need to add an additional possession for the player leaving the game. Lastly, if "time" is True, then the previous play was a timeout, and the last rebound was the same time as the timeout, and the rebounding team was the defense. If this is all true, then we do not need to add another possession since the rebound took care of that.
            for sub in floor:
                if sub.id == play["Person1"]:
                    spot = floor.index(sub)
                    if playClock != play["PC_Time"] and turnoverClock != play["PC_Time"] and not time:
                        #print(play["Event_Num"])
                        if sub.team == play["Team_id"]:
                            sub.offPos += 1
                        else:
                            sub.defPos += 1
# Next to check is the variable "turnover", which is only True when a foul is called right after a turnover, and the fouling team is the same as the turnover team. If this is the case, then the player leaving the floor needs to have another possession added to their total.
                    if turnover:
                        if sub.team == teamTurnover:
                            sub.defPos += 1
                        else:
                            sub.offPos += 1
# The last check in the first section was made to handle the situation where the rebounder is not on the floor yet, since the order of events was recorded incorrectly. So if the time of the play is the same as the reboundTime of the player not on the floor yet, then the player leaving the floor for the rebounder was already off the floor, so we subtract a possession from that person.
                    if reboundTime == play["PC_Time"] and follow:
                        if sub.team == teamShot:
                            sub.offPos -= 1
                        else:
                            sub.defPos -= 1
# Then we go through the roster and find the person who is being subbed in from the bench and insert that player into the index of the sub.
                    for bench in roster:
                        if bench.id == play["Person2"]:
# This is the same check as above when the rebounder is not on the floor yet. That means that the people who get subbed in after the rebound were actually on the floor for the rebound, so they must also be given an extra offensive possession.
                            if reboundTime == play["PC_Time"] and follow:
                                if bench.team == teamShot:
                                    bench.offPos += 1
                                else:
                                    bench.defPos += 1
# If the foulClock is the same as the current time of the play, then this sub is taken during a foul, which could have free throws. So we add the player to the heldSubs list to execute later. If the sub is not done during a foul, then we change the spot of the floor to the person coming on from the bench.
                            if foulClock == play["PC_Time"]:
                                heldSubs.append([spot,bench])
                            else:
                                floor[spot] = bench
                            break
                    break

# This is the case of a timeout being called. The only time this is influencial on a play is if the timeout is taken immediately after a rebound. If this is true, then we need ot make sure not to add a possession any players who may be subsequently subbed off after the timeout is taken. If it is an offensive rebound though, then the subsequent subs would need to add a possession, so we set the variable "time" back to False.
        elif play["Event_Msg_Type"] == 9:
            if play["PC_Time"] == reboundTime:
                time = True
                if offenseReboundingTeam:
                    time = False
# This is the end of a quarter, which could also be the end of the game, so whichever team is holding the ball gets an extra offesnive possession, and the other team gets a defensive possession.
        elif play["Event_Msg_Type"] == 13:
            possessionOnly(play["Team_id"])

# Event_Msg_Type "16" is the end of a game.
        elif play["Event_Msg_Type"] == 16:
# Since the game is over, we now will add all of the players to the output file with the required statistics.
            for player in roster:
# If a player has not offensive or defensive possessions, then they never entered the game, so they may have been inactive, or just never saw the floor. In any case, they get an N/A for both offensive and defensive ratings.
                if player.offPos == 0:
                    offensiveRating = "N/A"
                else:
                    offense = 100*(player.pointsFor/player.offPos)
                    offensiveRating = math.floor( offense * 10 + 0.5)/10

                if player.defPos == 0:
                    defensiveRating = "N/A"
                else:
                    defense = round(100*player.pointsAgainst/player.defPos,1)
                    defensiveRating = math.floor( defense * 10 + 0.5)/10

                output.writerow([play["Game_id"], player.id, offensiveRating, defensiveRating])

            del roster[:], floor[:]
