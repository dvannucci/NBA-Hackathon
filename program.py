import csv

class Player:
    def __init__(self, team, id):
        self.team = team
        self.id = id
        self.pointsFor = 0
        self.pointsAgainst = 0
        self.offPos = 0
        self.defPos = 0

    def offensive(self, points):
        self.pointsFor += points
        self.offPos += 1

    def defensive(self, points):
        self.pointsAgainst += points
        self.defPos += 1


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


"""
# Reads each line of the plays file until the end. MAIN OUTER LOOP
for line in plays:
    line = line.split()
    print(line)
    game = line[playsGameIndex]
    print(game)
    exit(0)
"""


line = lineup.readline()
line = line.split()

roster = []
floor = []

# WITHIN THE CASE FOR 12,0 WHICH IS THE START OF THE GAME.
while line[lineupPeriodIndex] == "0":
    roster.append(Player(line[lineupTeamIndex], line[lineupPersonIndex]))
    line = lineup.readline()
    line = line.split()

while line[lineupPeriodIndex] == "1":
    for x in roster:
        if x.id == line[lineupPersonIndex]:
            floor.append(x)
            break
    line = lineup.readline()
    line = line.split()


print("Roster:")
for x in roster:
    print(x.id)

print("\n\n")

print("Floor:")
for z in floor:
    print(z.id)

floor[0].offensive(4)

floor[0] = roster[3]

print("Roster:")
for x in roster:
    print(x.id)

print("\n\n")

print("Floor:")
for z in floor:
    print(z.id)

print(roster[2].pointsFor)
print(roster[0].pointsFor)
