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


# Opens all files provided.
plays = open("Play_by_Play.txt", "r")
codes = open("Event_Codes.txt", "r")
lineup = open("Game_Lineup.txt", "r")

# Creates a new .csv file and puts it in csv writer mode.
answer = open("answer.csv", "w")
output = csv.writer(answer)

# Writes the column headers in the answer file in .csv format
answerHeaders = ["Game_ID", "Player_ID", "OffRtg", "DefRtg"]
output.writerow(answerHeaders)

#Reads the first line of the Play_by_Play.txt file to know which column each data type is in.
playHeaders = plays.readline()
playHeaders = playHeaders.split()

# Sets a variable to all index's of the necessary data. Have to do this just in case the order of the columns changed. Not sure if this is necessary, but thought I could include it and we can decide later if we wanna keep it.
playsGameIndex = playHeaders.index('"Game_id"')
messageTypeIndex = playHeaders.index('"Event_Msg_Type"')
playsPeriodIndex = playHeaders.index('"Period"')
actiontypeindex = playHeaders.index('"Action_Type"')
option1Index = playHeaders.index('"Option1"')
option2Index = playHeaders.index('"Option2"')
option3Index = playHeaders.index('"Option3"')
playsTeamIndex = playHeaders.index('"Team_id"')
playsPerson1Index = playHeaders.index('"Person1"')
person2Index = playHeaders.index('"Person2"')
person3Index = playHeaders.index('"Person3"')

# Reads the first line of the Game_Lineup.txt file to know which column each data type is in.
lineupHeaders = lineup.readline()
lineupHeaders = lineupHeaders.split()

# Sets a variable to all index's of the necessary data. Same thing as above, not sure if we keep this or not.
lineupGameIndex = lineupHeaders.index('"Game_id"')
lineupPeriodIndex = lineupHeaders.index('"Period"')
lineupPersonIndex = lineupHeaders.index('"Person_id"')
lineupTeamIndex = lineupHeaders.index('"Team_id"')

# These are the two lists needed to keep track of the roster of everyone in the game, as well as everyone on the floor.
roster = []
floor = []

# Reads each line of the plays file until the end. MAIN OUTER LOOP.
for play in plays:
    play = play.split()

# If the messageTypeIndex is equal to "12", then this is the start of a period. This is an administration step which does not deal with any actual basketball plays.
    if play[messageTypeIndex] == "12":
# If the period of this play is equal to "1", then this is the start of a new game, so we must change the "game" variable and fill the roster and floor lists appropriately.
        if play[playsPeriodIndex] == "1":
            game = play[playsGameIndex]
# This for loop now goes through the Game_Lineup file.
            for gameLine in iter(lineup.readline, ''):
                gameLine = gameLine.split()
# If the period of the read line is "0", this is showing the players that are present at the game. For each player present, a new object is created with the players id, and the team. The object is then appended to the roster list.
                if gameLine[lineupPeriodIndex] == "0":
                    roster.append(Player(gameLine[lineupTeamIndex], gameLine[lineupPersonIndex]))
# If the period of the read line is "1", these are the players that start on the floor at the beginning of the first quarter. So they must be found on the roster list, and appended to the floor list.
                elif gameLine[lineupPeriodIndex] == "1":
                    for x in roster:
                        if x.id == gameLine[lineupPersonIndex]:
                            floor.append(x)
                            break
# If the period is no longer "0" or "1", then we are finished filling the roster and floor lists, so we put the file cursor back one line so that the next time we read the Game_Lineup file, it will be starting in the correct spot.
                else:
                    lineup.seek(previous)
                    break
# This is the variable that holds the placement of the previous line in the Game_Lineup file.
                previous = lineup.tell()
# If the the period of the play is not equal to "1", then the messageTypeIndex of "12" is referring to the start of a new quarter. There may have been substitutions during the quarter break, so we must go through the Game_Lineup and change the floor list accordingly.
        else:
# Assign a variable called period which is the number of the new quarter.
            period = play[playsPeriodIndex]
# Delete the old list of the players on the floor.
            del floor[:]
# Go through the new players who should be on the floor, find them in the total roster list, and append them the the floor list.
            for gameLine in iter(lineup.readline, ''):
                gameLine = gameLine.split()
# Only do this for as long as the lineup period is the same as the period of the last play.
                if gameLine[lineupPeriodIndex] == period:
                    for x in roster:
                        if x.id == gameLine[lineupPersonIndex]:
                            floor.append(x)
                            break
# Same process as above, we just replace the pointer in the file back a line where it should be for the next iteration of reading the Game_Lineup file.
                else:
                    lineup.seek(previous)
                    break

                previous = lineup.tell()


# This is now the main section which will deal with the various types of plays and scenarios that could happen in the game.
    if play[messageTypeIndex] == "12":
    break


print("Roster:")
for x in roster:
    print(x.id)

print("\n\n")

print("Floor:")
for z in floor:
    print(z.id)
