import pandas as pd
import numpy as np
import csv

class Player:
    def __init__(self, team, id):
        self.team = team
        self.id = id
        self.pointsWhileOnFloor = 0
        self.pointsAgainst = 0
        self.pointsPersonal = 0
        self.offPos = 0
        self.defPos = 0
        self.freeThrowsMade = 0
        self.freeThrowsAttempted = 0
        self.fieldGoalsMade = 0
        self.fieldGoalsAttempted = 0
        self.minutesPlayed = 0
        self.assists = 0
        self.steals = 0
        self.blocks = 0
        self.personalFouls = 0
        self.offensiveRebounds = 0
        self.defensiveRebounds = 0
        self.turnovers = 0
        self.threePointers = 0
        self.quarterEntered = 0
        self.timeEntered = 0

    def offensivePointsAndPossession(self, points):
        self.pointsWhileOnFloor += points
        self.offPos += 1

    def defensivePointsAndPossession(self, points):
        self.pointsAgainst += points
        self.defPos += 1

    def offensivePoints(self, points):
        self.pointsWhileOnFloor += points

    def defensivePoints(self, points):
        self.pointsAgainst += points

    def offensivePossession(self):
        self.offPos += 1

    def defensivePossession(self):
        self.defPos += 1

class Team:
    def __init__(self, team):
        self.team = team
        self.offensiveRebounds = 0
        self.totalRebounds = 0
        self.minutesPlayed = 0
        self.assists = 0
        self.fieldGoalsMade = 0
        self.fieldGoalsAttempted = 0
        self.pointsTeam = 0
        self.freeThrowsMade = 0
        self.freeThrowsAttempted = 0
        self.turnovers = 0
        self.threePointers = 0
        self.scoringPossessions = 0
        self.offensiveReboundWeight = 0
        self.offensiveReboundPercentage = 0
        self.playPercentage = 0
#Defensive
        self.defensiveOffensiveReboundPercentage = 0
        self.defensiveFieldGoalPercentage = 0
        self.FMWT = 0
        self.blocks = 0
        self.steals = 0
        self.personalFouls = 0
        self.teamPossessions = 0
        self.teamDefensiveRating = 0


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

def teamHelper(own, opponent):
# Offensive stuff
    teams[own].scoringPossessions = teams[own].fieldGoalsMade + (1 - (1 - (teams[own].freeThrowsMade / teams[own].freeThrowsAttempted))**2) * teams[own].freeThrowsAttempted * 0.4

    teams[own].offensiveReboundPercentage = teams[own].offensiveRebounds / (teams[own].offensiveRebounds + (teams[opponent].totalRebounds - teams[opponent].offensiveRebounds))

    teams[own].playPercentage = teams[own].scoringPossessions / (teams[own].fieldGoalsAttempted + teams[own].freeThrowsAttempted * 0.4 + teams[own].turnovers)

    teams[own].offensiveReboundWeight = ((1 - teams[own].offensiveReboundPercentage) * teams[own].playPercentage) / ((1 - teams[own].offensiveReboundPercentage) * teams[own].playPercentage +  teams[own].offensiveReboundPercentage * (1 - teams[own].playPercentage))
#Defensive stuff
    teams[own].defensiveOffensiveReboundPercentage = teams[opponent].offensiveRebounds / (teams[opponent].offensiveRebounds + (teams[own].totalRebounds - teams[own].offensiveRebounds))

    teams[own].defensiveFieldGoalPercentage = teams[opponent].fieldGoalsMade / teams[opponent].fieldGoalsAttempted

    teams[own].FMWT = (teams[own].defensiveFieldGoalPercentage * (1 - teams[own].defensiveOffensiveReboundPercentage)) / (teams[own].defensiveFieldGoalPercentage * (1 - teams[own].defensiveOffensiveReboundPercentage) + (1 - teams[own].defensiveFieldGoalPercentage) * teams[own].defensiveOffensiveReboundPercentage)

    teams[own].teamPossessions =  0.5 * ((teams[own].fieldGoalsAttempted + 0.4 * teams[own].freeThrowsAttempted - 1.07 * (teams[own].offensiveRebounds / (teams[own].offensiveRebounds + (teams[opponent].totalRebounds - teams[opponent].offensiveRebounds))) * (teams[own].fieldGoalsAttempted - teams[own].fieldGoalsMade) + teams[own].turnovers) + (teams[opponent].fieldGoalsAttempted + 0.4 * teams[opponent].freeThrowsAttempted - 1.07 * (teams[opponent].offensiveRebounds / (teams[opponent].offensiveRebounds + (teams[own].totalRebounds - teams[own].offensiveRebounds))) * (teams[opponent].fieldGoalsAttempted - teams[opponent].fieldGoalsMade) + teams[opponent].turnovers))

    teams[own].teamDefensiveRating = 100 * (teams[opponent].pointsTeam / teams[own].teamPossessions)

    teams[own].defensivePointsPerScoringPossession = teams[opponent].pointsTeam / (teams[opponent].fieldGoalsMade + (1 - (1 - (teams[opponent].freeThrowsMade / teams[opponent].freeThrowsAttempted))**2) * teams[opponent].freeThrowsAttempted * 0.4)


def teamStats(own):
    teams[own].minutesPlayed += player.minutesPlayed
    teams[own].assists += player.assists
    teams[own].fieldGoalsMade += player.fieldGoalsMade
    teams[own].fieldGoalsAttempted += player.fieldGoalsAttempted
    teams[own].pointsTeam += player.pointsPersonal
    teams[own].freeThrowsMade += player.freeThrowsMade
    teams[own].freeThrowsAttempted += player.freeThrowsAttempted
    teams[own].turnovers += player.turnovers
    teams[own].threePointers += player.threePointers
    teams[own].blocks += player.blocks
    teams[own].steals += player.steals
    teams[own].personalFouls += player.personalFouls

def offensiveRating(own):

    qAst = ((player.minutesPlayed / (teams[own].minutesPlayed / 5)) * (1.14 * ((teams[own].assists - player.assists) / teams[own].fieldGoalsMade))) + ((((teams[own].assists / teams[own].minutesPlayed) * player.minutesPlayed * 5 - player.assists) / ((teams[own].fieldGoalsMade / teams[own].minutesPlayed) * player.minutesPlayed * 5 - player.fieldGoalsMade)) * (1 - (player.minutesPlayed / (teams[own].minutesPlayed / 5))))

    fieldGoalPart = player.fieldGoalsMade * (1 - 0.5 * ((player.pointsPersonal - player.freeThrowsMade) / (2 * player.fieldGoalsAttempted)) * qAst)

    assistPart = 0.5 * (((teams[own].pointsTeam - teams[own].freeThrowsMade) - (player.pointsPersonal - player.freeThrowsMade)) / (2 * (teams[own].fieldGoalsAttempted - player.fieldGoalsAttempted))) * player.assists

    if player.freeThrowsAttempted == 0:
        freeThrowPart = 0
        freeThrowsMissedPossessions = 0
    else:
        freeThrowPart = (1-(1-(player.freeThrowsMade/player.freeThrowsAttempted))**2)*0.4*player.freeThrowsAttempted
        freeThrowsMissedPossessions = ((1 - (player.freeThrowsMade / player.freeThrowsAttempted))**2) * 0.4 * player.freeThrowsAttempted

    offensiveReboundPart = player.offensiveRebounds * teams[own].offensiveReboundWeight * teams[own].playPercentage

    scoringPossessions = (fieldGoalPart + assistPart + freeThrowPart) * (1 - (teams[own].offensiveRebounds / teams[own].scoringPossessions) * teams[own].offensiveReboundWeight * teams[own].playPercentage) + offensiveReboundPart

    fieldGoalsMissedPossessions = (player.fieldGoalsAttempted - player.fieldGoalsMade) * (1 - 1.07 * teams[own].offensiveReboundPercentage)



    totalPossessions = scoringPossessions + fieldGoalsMissedPossessions + freeThrowsMissedPossessions + player.turnovers



    pointsProducedFieldGoals = 2 * (player.fieldGoalsMade + 0.5 * player.threePointers) * (1 - 0.5 * ((player.pointsPersonal - player.freeThrowsMade) / (2 * player.fieldGoalsAttempted)) * qAst)

    pointsProducedAssists = 2 * ((teams[own].fieldGoalsMade - player.fieldGoalsMade + 0.5 * (teams[own].threePointers - player.threePointers)) / (teams[own].fieldGoalsMade - player.fieldGoalsMade)) * 0.5 * (((teams[own].pointsTeam - teams[own].freeThrowsMade) - (player.pointsPersonal - player.freeThrowsMade)) / (2 * (teams[own].fieldGoalsAttempted - player.fieldGoalsAttempted))) * player.assists

    pointsProducedOffensiveRebounds = player.offensiveRebounds * teams[own].offensiveReboundWeight * teams[own].playPercentage * (teams[own].pointsTeam / (teams[own].fieldGoalsMade + (1 - (1 - (teams[own].freeThrowsMade / teams[own].freeThrowsAttempted))**2) * 0.4 * teams[own].freeThrowsAttempted))

    pointsProduced = (pointsProducedFieldGoals + pointsProducedAssists + player.freeThrowsMade) * (1 - (teams[own].offensiveRebounds / teams[own].scoringPossessions) * teams[own].offensiveReboundWeight * teams[own].playPercentage) + pointsProducedOffensiveRebounds

    return round(100 * (pointsProduced / totalPossessions))

def defensiveRating(own, opponent):

    stopsOne = player.steals + player.blocks * teams[own].FMWT * (1 - 1.07 * teams[own].defensiveOffensiveReboundPercentage) + player.defensiveRebounds * (1 - teams[own].FMWT)

    stopsTwo = (((teams[opponent].fieldGoalsAttempted - teams[opponent].fieldGoalsMade - teams[own].blocks) / teams[own].minutesPlayed) * teams[own].FMWT * (1 - 1.07 * teams[own].defensiveOffensiveReboundPercentage) + ((teams[opponent].turnovers - teams[own].steals) / teams[own].minutesPlayed)) * player.minutesPlayed + (player.personalFouls / teams[own].personalFouls) * 0.4 * teams[opponent].freeThrowsAttempted * (1 - (teams[opponent].freeThrowsMade / teams[opponent].freeThrowsAttempted))**2


    stopPercentage = ((stopsOne + stopsTwo) * teams[opponent].minutesPlayed) / (teams[own].teamPossessions * player.minutesPlayed)


    return round(teams[own].teamDefensiveRating + 0.2 * (100 * teams[own].defensivePointsPerScoringPossession * (1 - stopPercentage) - teams[own].teamDefensiveRating))



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
teams = []

# These two lists will be used in the case of free throws. There are many different types of free throws, but we can split all but one of them into two distinct groups. The separator being whether they are reboundable or not.
freeThrowActionsNoRebound = [11,13,14,16,17,18,19,20,21,22,25,26,27,28,29]
freeThrowActionsRebound = [12,15]

# This is a boolean variable, which will be used in the occasional case when on a rebound play, we are not told who has secured the rebound. When this happens, whatever the team is of the next play following, that is the team that secured the previous plays rebound. So when this is set to "True", we will verify the team. It must originally be set to "false".
needToCheck = False

# This is a boolean variable which will be used when a foul is committed and there is a possible free throw situation. This will freeze substitutions for the time, so correct stats can be recorded. The list will hold the substitutions that must be made after the final free throws are complete.
subFreeze = False
heldSubs = []

# This is the main outer loop grouping all the plays by game.
for game,group in playFile.groupby("Game_id"):
# Sort the game on the basis of the world clock time first, and then on event number. This gives the true ordering for the game.
    sortedGameData = group.sort_values(by=["WC_Time","Event_Num"])


# MAYBE HAVE TO DELETE HERE, MAYBE HAVE TO DELETE WHEN PUTTING THE DATA INTO THE OUTPUT FILE.

    del roster[:], floor[:], teams[:]
# Whenever a new game begins, we must fill the roster list, as well as the floor list. To do this, we go into the lineup data and get the group that has the correct Game_id, and has a period of zero.
    GameLineBeginning = lineup.get_group((game,0))
# This step uses a list comprehension to create a new object for every player at the start of a game, and creates a roster list. So it takes the Team_id and the Person_id from every row in the game's data frame, and makes the structure and the list.
    roster = [Player(player["Team_id"],player["Person_id"]) for index,player in GameLineBeginning.iterrows()]
# We then have to fill the floor list. To do that, we look in the lineup data again, and get the group of the same game, but with period of one.
    GameLineQuarter1 = lineup.get_group((game, 1))
# Using list comprehsion again, we add every athlete from the roster list, only if they're on the floor at the beginning of the game, making them a starter.
    floor = [athlete for athlete in roster if any(athlete.id == starter["Person_id"] for index,starter in GameLineQuarter1.iterrows())]
# For each player that starts out on the floor, we must set their "quarterEntered" and "timeEntered" variables to the beginning of the game. These will be used later for substitutions to figure out how many minutes each player plays.
    for player in floor:
        player.quarterEntered = 1
        player.timeEntered = 7200
# Here we are creating the two team objects which we will use to track the various team stats needed for the offensive and defensive rating calculations. We need an extra list called "hold" which we use to only go through as many players as we need from the floor to construct the two teams data structures.
    hold = []
    for player in floor:
        if len(hold) == 2:
            break
        elif player.team not in hold:
            hold.append(player.team)
            teams.append(Team(player.team))

# Now that the roster and floor lists are filled, we go through each play of the game.
    for index,play in sortedGameData.iterrows():

# This statement only executed when the previous play is a rebound, but not by a player on the floor. It is a team rebound, and we can verify the team since on the following play, the "Team_id" will be who got the previous rebound.
        if needToCheck:
            if play["Team_id"] != teamShot:
                possessionOnly(teamShot)
            needToCheck = False

# This statement will only execute in the case that "subFreeze" has been set to true, meaning that in one of the most recent plays, there has been a foul called. If this has happened, but the current play is not a free throw, "3", or a substitution, "8", then the freeze is unnecessary, since there is no reason to put off the substitution. So we make the freeze equal to false, and execute any substitutions that were saved in the "heldSubs" list.
        if subFreeze and play["Event_Msg_Type"] != 3 and play["Event_Msg_Type"] != 8:
            subFreeze = False
            if heldSubs:
                for spot,bench in heldSubs:
                    floor[spot] = bench
                del heldSubs[:]

# If the Event_Msg_Type is equal to "12", and the period is greater than "1", then this is the start of a period that is not the start of a game. Here we must just change the floor lineup in case of a substitution during th quarter break.
        if play["Event_Msg_Type"] == 12 and play["Period"] > 1:
# Exact same logic as above when we filled the floor list at the beginning of a game.
            GameLineNewQuarter = lineup.get_group((game, play["Period"]))

            spots = []
            hold = [new["Person_id"] for index,new in GameLineNewQuarter.iterrows()]

            for player in floor:
                if player.id not in hold:
                    spots.append(floor.index(player))
                    player.minutesPlayed += (player.timeEntered/600) + ((play["Period"] -player.quarterEntered - 1) * 12)


            for index in spots:
                for player in roster:
                    if player.id in hold and player not in floor:
                        floor[index] = player
                        floor[index].quarterEntered = play["Period"]
                        floor[index].timeEntered = 7200
                        break


# If the Event_Msg_Type is a "1", then it's a made shot, which is the end of a possession. For every player on the floor, depending on their team, call the function to add to their offensive or defensive stats.
        elif play["Event_Msg_Type"] == 1:
            pointsAndPossession(play["Option1"])
            for player in floor:
                if player.id == play["Person1"]:
                    player.fieldGoalsMade += 1
                    player.fieldGoalsAttempted += 1
                    player.pointsPersonal += play["Option1"]
                    if play["Option1"] == 3:
                        player.threePointers += 1
                if player.id == play["Person2"]:
                    player.assists += 1

# If the shot has been missed, we set the variable "teamShot" to the team that took the shot. Since every missed shot is followed by a rebound, we must check on the rebound play if it was an offensive or defensive rebound.
        elif play["Event_Msg_Type"] == 2:
            teamShot = play["Team_id"]
            for player in floor:
                if player.id == play["Person1"]:
                    player.fieldGoalsAttempted += 1
                elif player.id == play["Person3"]:
                    player.blocks += 1

# An Event_Msg_Type of "3" is a free throw which has a few different types.
        elif play["Event_Msg_Type"] == 3:
# No matter the outcome of the free throw, an attempt will be added to the player attempting the free throw.
            for player in floor:
                if player.id == play["Person1"]:
                    player.freeThrowsAttempted += 1
                    break
# Stand alone special case: If Action_Type is "10", and the Option1 is "1", then this was a made "and one" free throw, so we add the stats to the players on the court, but we do not add a possession since it was already added on the made shot since this is an "and one". We also set "subFreeze" to false, since it may be true at this time, but now since the final free throw of the possession has been made, the new players can come onto the floor now
            if play["Action_Type"] == 10 and play["Option1"] == 1:
                pointsOnly(play["Option1"])
                player.freeThrowsMade += 1
                player.pointsPersonal += 1
# This group will only add points and no possessions since no possession change is possible when there are no rebounds. We must put the "if play["Option1"]" statement inside of the outer if statement because if the free throw is missed, nothing happens to any players points or possessions. If it was on the outside condition, like on the free throws with rebounds in the next "elif", then execution would fall to the "else" statement at the end, and would unnecessarily keep track of the team who shot the free throw.
            elif play["Action_Type"] in freeThrowActionsNoRebound:
                if play["Option1"] == 1:
                    pointsOnly(play["Option1"])
                    player.freeThrowsMade += 1
                    player.pointsPersonal += 1
# This group will add points and possessions if the free throw is made, since rebounds were possible.
            elif play["Action_Type"] in freeThrowActionsRebound and play["Option1"] == 1:
                pointsAndPossession(play["Option1"])
                player.freeThrowsMade += 1
                player.pointsPersonal += 1
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
# After the loop completes, if rebounder is still "None", then this is the case of a team rebound, which must be handled separately. We set the variable "needToCheck" equal to true, which will bring us into an "if" statement on the next loop, and will verify the rebounding team.
            if rebounder is None:
                needToCheck = True

# If the team of the rebounder is different then "teamShot", then the opposing team to the shooting team got the rebound. This results in a possession change, but since no points were scored, we only add the appropriate offensive or defensive possessions to the players on the floor. If the rebounder's team is the same as "teamShot", then this was an offensive rebound, so we can ignore it since no possession changes, and no points were scored.
            elif rebounder.team != teamShot:
                possessionOnly(teamShot)
                rebounder.defensiveRebounds += 1
                for team in teams:
                    if rebounder.team == team.team:
                        team.totalRebounds += 1
                        break

            else:
                for player in floor:
                    if player.id == play["Person1"]:
                        player.offensiveRebounds += 1
                        for team in teams:
                            if player.team == team.team:
                                team.offensiveRebounds += 1
                                team.totalRebounds += 1
                                break
                        break

# If the Event_Msg_Type is a "5", this is a turnover. Therefore, we just add the appropriate possessions to the players on the floor, and no points. Offensive possessions are given to the team that committed the turnover.
        elif play["Event_Msg_Type"] == 5:
            possessionOnly(play["Team_id"])
            for player in floor:
                if player.id == play["Person1"]:
                    player.turnovers += 1
                elif player.id == play["Person2"]:
                    player.steals += 1

# If a foul is committed on a play,then we must freeze all substitutions for the time being. If any substitutions are made during free throws, then we must wait until after the free throws go through to before making the substitutions.
        elif play["Event_Msg_Type"] == 6:
            for player in floor:
                if player.id == play["Person1"]:
                    player.personalFouls += 1
                    break
            subFreeze = True

# If the Event_Msg_Type is an "8", this is a substitution. Person1 is leaving the game, person2 is entering the game.
        elif play["Event_Msg_Type"] == 8:
# First we need to check all players on the floor to figure out the index of who needs to be subbed out in the floor list. After the spot is found, then we go through the roster and find the person who is being subbed in from the bench and insert that player into the index of the sub.
            for sub in floor:
                if sub.id == play["Person1"]:
                    spot = floor.index(sub)

                    if sub.quarterEntered == play["Period"]:
                        sub.minutesPlayed += (sub.timeEntered - play["PC_Time"])/600
                    else:
                        sub.minutesPlayed += ((sub.timeEntered/600) + ((play["Period"] - sub.quarterEntered - 1) * 12) + ((7200 - play["PC_Time"])/600))

                    for bench in roster:
                        if bench.id == play["Person2"]:
                            bench.timeEntered = play["PC_Time"]
                            bench.quarterEntered = play["Period"]
                            if subFreeze:
                                heldSubs.append([spot,bench])
                            else:
                                floor[spot] = bench
                            break
                    break


        elif play["Event_Msg_Type"] == 13:
            possessionOnly(play["Team_id"])


        elif play["Event_Msg_Type"] == 16:

            for player in floor:
                if player.quarterEntered == play["Period"]:
                    player.minutesPlayed += (player.timeEntered - play["PC_Time"])/600
                else:
                    player.minutesPlayed += ((player.timeEntered/600) + ((play["Period"] - player.quarterEntered - 1) * 12) + ((7200 - play["PC_Time"])/600))

            for player in roster:
                if player.team == teams[0].team:
                    teamStats(0)

                else:
                    teamStats(1)
            teams[1].minutesPlayed = 240.0

            teamHelper(0,1)

            teamHelper(1,0)


            #print(teams[1].team)
            #print(teams[1].offensiveRebounds)
            #print(teams[1].totalRebounds)
            #print(teams[1].minutesPlayed)
            #print(teams[1].assists)
            #print(teams[1].fieldGoalsMade)
            #print(teams[1].fieldGoalsAttempted)
            #print(teams[1].pointsTeam)
            #print(teams[1].freeThrowsMade)
            #print(teams[1].freeThrowsAttempted)
            #print(teams[1].turnovers)
            #print(teams[1].threePointers)
            #print(teams[1].scoringPossessions)
            #print(teams[1].offensiveReboundWeight)
            #print(teams[1].offensiveReboundPercentage)
            #print(teams[1].playPercentage)
            #print(teams[1].defensiveOffensiveReboundPercentage)
            #print(teams[1].defensiveFieldGoalPercentage)
            #print(teams[1].FMWT)
            #print(teams[1].blocks)
            #print(teams[1].steals)
            #print(teams[1].personalFouls)
            #print(teams[1].teamPossessions)
            #print(teams[1].teamDefensiveRating)


            #exit(0)



            for player in roster:
                if player.minutesPlayed == 0:
                    output.writerow([play["Game_id"],player.id,"N/A", "N/A"])

                elif player.team == teams[0].team:
                    output.writerow([play["Game_id"], player.id, offensiveRating(0), defensiveRating(0,1)])

                else:
                    output.writerow([play["Game_id"], player.id, offensiveRating(1), defensiveRating(1,0)])

            #exit(0)
            print(roster[26].id)
            print(roster[26].pointsWhileOnFloor)
            print(roster[26].pointsAgainst)
            print(roster[26].pointsPersonal)
            print(roster[26].offPos)
            print(roster[26].defPos)
            print(roster[26].freeThrowsMade)
            print(roster[26].freeThrowsAttempted)
            print(roster[26].fieldGoalsMade)
            print(roster[26].fieldGoalsAttempted)
            print(roster[26].minutesPlayed)
            print(roster[26].assists)
            print(roster[26].steals)
            print(roster[26].blocks)
            print(roster[26].personalFouls)
            print(roster[26].offensiveRebounds)
            print(roster[26].defensiveRebounds)
            print(roster[26].turnovers)
            print(roster[26].threePointers)
            print(roster[26].quarterEntered)
            print(roster[26].timeEntered)
            exit(0)


        elif play["Event_Msg_Type"] == 12 or play["Event_Msg_Type"] == 10 or play["Event_Msg_Type"] == 7 or play["Event_Msg_Type"] == 9 or play["Event_Msg_Type"] == 20 or play["Event_Msg_Type"] == 18 or play["Event_Msg_Type"] == 13:
            continue

        else:
            subFreeze = True
            print(play)
            exit(0)
