def getUnsignedInt(message):
	retVal = -1
	while (retVal == -1):
		try:
			retVal = int(input(message))
		except ValueError:
			print("The entered value isn't a valid integer. Try again...")
			retVal = -1
			continue
		if (retVal <= 0):
			print("The entered value isn't valid. Try again...")
			retVal = -1
	print()
	return retVal

def printWordsearchGrid(width, height, word, positions):
	colors = {
		"reset": "\033[0m",
		"normal": "\033[37m",
		"not found": "\033[91m",
		"found": "\033[92m",
		"chars": "\033[93m"
	}
	if (len(positions) == 0):
		print("{}The word \"{}\" wasn't found.{}\n".format(colors["not found"], word, colors["reset"]))
		return
	matrix, emptyValue = [], "•"
	#enter the matrix
	matrix.append([colors["normal"] + " "] + list(str(i)[-1] for i in range(1, width + 1)) + [" "])
	matrix.append(["╔"] + list("═" for _ in range(width)) + ["╗"])
	for i in range(1, height + 1):
		matrix.append(["║"] + list(emptyValue for _ in range(width)) + ["║", str(i)])	
	matrix.append(["╚"] + list("═" for _ in range(width)) + ["╝" + colors["reset"]])

	for i in positions:
		currentLetterIndex = 0
		while (i[0] != i[2] or i[1] != i[3]):
			matrix[i[1] + 2][i[0] + 1] = colors["chars"] + word[currentLetterIndex] + colors["reset"]
			i[0] += 1 if i[2] > i[0] else -1 if i[2] < i[0] else 0
			i[1] += 1 if i[3] > i[1] else -1 if i[3] < i[1] else 0
			currentLetterIndex += 1
		matrix[i[1] + 2][i[0] + 1] = colors["chars"] + word[currentLetterIndex] + colors["reset"]

	print("{}The word \"{}\" was found {}:{}\n".format(colors["found"], word, "once" if len(positions) == 1 else str(len(positions)) + " times", colors["reset"]))
	for i in matrix:
		print(" {}".format("".join(i)))
	print()

# -- get the user input -- #
rowAmount = getUnsignedInt("Enter the amount of rows in the crossword: ")
rows = []
rowLength = -1
for i in range(rowAmount):
	correctValue = False
	while (not correctValue):
		enteredValue = input("Enter the value for row #{}{}: ".format("0" * (len(str(rowAmount)) - len(str(i + 1))), i + 1))
		if (rowLength == -1):
			rowLength = len(enteredValue)
			correctValue = True
			rows.append(enteredValue.upper())
		elif (rowLength != len(enteredValue)):
			print("The entered text length won't create a rectangle. Try again...\n")
		else:
			rows.append(enteredValue.upper())
			correctValue = True

wordAmount = getUnsignedInt("\nEnter the amount of words to find: ")
words = []
for i in range(wordAmount):
	correctValue = False
	while (not correctValue):
		enteredValue = input("Enter the word #{}{}: ".format("0" * (len(str(rowAmount)) - len(str(i + 1))), i + 1))
		if (enteredValue == ""):
			print("The entered text isn't valid. Try again...\n")
		else:
			words.append(enteredValue.upper())
			correctValue = True

# -- get the lines of text -- #
linesToCheck = []

#left to right
linesToCheck.append(rows[:])

#right to left
for i in range(len(rows)):
	rows[i] = rows[i][::-1]
linesToCheck.append(rows[:])

for i in range(len(rows)):
	rows[i] = rows[i][::-1]
columns = []

#top to bottom
for i in range(rowLength):
	outputString = ""
	for j in range(len(rows)):
		outputString += rows[j][i]
	columns.append(outputString)
linesToCheck.append(columns[:])

#bottom to top
for i in range(len(columns)):
	columns[i] = columns[i][::-1]
linesToCheck.append(columns[:])

#zig-zag right-top to left-bottom
currentX, currentY, diagonals = rowLength - 1, 0, []
while (currentX != 0 or currentY != len(rows)):
	tempX, tempY, tempString = currentX, currentY, []

	while (tempX != rowLength and tempY != len(rows)):
		tempString.append(rows[tempY][tempX])
		tempX += 1
		tempY += 1

	diagonals.append("".join(tempString))
	changedX = False
	if (currentX > 0):
		currentX -= 1
		changedX = True
	currentY = currentY + 1 if not changedX else currentY
linesToCheck.append(diagonals[:])

#zig-zag right-top to left-bottom reversed
for i in range(len(diagonals)):
	diagonals[i] = diagonals[i][::-1]
linesToCheck.append(diagonals[:])

#zig-zag left-top to right-bottom
currentX, currentY, diagonals = rowLength - 1, len(rows) - 1, []
while (currentX != 0 or currentY != -1):
	tempX, tempY, tempString = currentX, currentY, []

	while (tempX != rowLength and tempY > -1):
		tempString.append(rows[tempY][tempX])
		tempX += 1
		tempY -= 1

	diagonals.append("".join(tempString))
	changedX = False
	if (currentX > 0):
		currentX -= 1
		changedX = True
	currentY = currentY - 1 if not changedX else currentY
linesToCheck.append(diagonals[:])

#zig-zag left-top to right-bottom reversed
for i in range(len(diagonals)):
	diagonals[i] = diagonals[i][::-1]
linesToCheck.append(diagonals[:])

# -- look for words in lines and save them into dictionary -- #
positions = {} # [x1, y1, x2, y2]

for i in range(len(linesToCheck)):
	for j in range(len(linesToCheck[i])):
		for k in range(len(words)):
			indexInLine = linesToCheck[i][j].find(words[k])
			if (indexInLine != -1):
				if (i == 0):	#left to right
					coordinates = [indexInLine, j, indexInLine + len(words[k]) - 1, j]
				elif (i == 1):	#right to left
					coordinates = [rowLength - indexInLine - 1, j, rowLength - indexInLine - len(words[k]), j]
				elif (i == 2):	#top to bottom
					coordinates = [j, indexInLine, j, indexInLine + len(words[k]) - 1]
				elif (i == 3):	#bottom to top
					coordinates = [j, len(rows) - indexInLine - 1, j, len(rows) - indexInLine - len(words[k])]			
				elif (i == 4):	#zig-zag right-top to left-bottom
					if (j < rowLength):
						coordinates = [rowLength - j - 1 + indexInLine, indexInLine, rowLength - j - 2 + indexInLine + len(words[k]), indexInLine + len(words[k]) - 1]
					else:
						coordinates = [indexInLine, j - rowLength + indexInLine + 1, indexInLine + len(words[k]) - 1, j - rowLength + indexInLine + len(words[k])]
				elif (i == 5):	#zig-zag right-top to left-bottom reversed
					if (j < rowAmount):
						coordinates = [rowLength - indexInLine - 1, j - indexInLine, rowLength - indexInLine - len(words[k]), j - indexInLine - len(words[k]) + 1]
					else:
						coordinates = [rowLength - j + rowAmount - 2 - indexInLine, rowAmount - indexInLine - 1, rowLength - j + rowAmount - 1 - len(words[k]) - indexInLine, rowAmount - indexInLine - len(words[k])]
				elif (i == 6):	#zig-zag left-top to right-bottom
					if (j < rowLength):
						coordinates = [rowLength - j - 1 + indexInLine, rowAmount - indexInLine - 1, rowLength - j - 2 + indexInLine + len(words[k]), rowAmount - indexInLine - len(words[k])]
					else:
						coordinates = [indexInLine, rowAmount - j + rowLength - 2 - indexInLine, indexInLine + len(words[k]) - 1, rowAmount - j + rowLength - indexInLine - len(words[k]) - 1]
				elif (i == 7):	#zig-zag left-top to right-bottom reversed
					if (j < rowAmount):
						coordinates = [rowLength - indexInLine - 1, rowAmount - j + indexInLine - 1, rowLength - indexInLine - len(words[k]), rowAmount - j + indexInLine + len(words[k]) - 2]
					else:
						coordinates = [rowAmount - j + rowLength - 2 - indexInLine, indexInLine, rowAmount - j + rowLength - indexInLine - len(words[k]) - 1, indexInLine + len(words[k]) - 1]

				if (words[k] not in positions):
					positions[words[k]] = [coordinates]
				else:
					positions[words[k]].append(coordinates)

# -- print out the results -- #
from os import system
from sys import platform
if (platform == "win32"):
	system("cls")
else:
	system("clear")

for i in words:
	printWordsearchGrid(rowLength, len(rows), i, positions[i] if i in positions else [])
input("Press ENTER to exit...")