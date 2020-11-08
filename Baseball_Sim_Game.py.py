import random

#setting up a new game
away = 0
home = 0

totPitchesAway = 0
totPitchesHome = 0

outs = 0

onFirst = 0
onSecond = 0
onThird = 0

inning = 1

next = 0

#get the teams playing from the user
team1 = input("Enter the away team")
team2 = input("Enter the home team")
print(team1 + " vs. " + team2)

atBat = team1 #set the away team to bat first

#function adds the number of runs scored to the batting team's score
#default number of runs is 1
def runScores(runners = 1):
	global away
	global home

	if atBat == team1:
		away += runners #away team scores
		print("Run scores " * runners)
		print(team1, ": ", away, " - ", team2, ": ", home) #print the score

	else:
		home += runners #home team scores
		print("Run scores " * runners)
		print(team1, ": ", away, " - ", team2, ": ", home) #print the score

#gets a random integer outcome from 1 to 1000
def getOutcome():
	return random.randint(1,1000)

#determines if a runner on third will go home and determines the outcome of the play at the plate
def goHome():
	global onThird
	global outs	

	go = getOutcome()
	print("Chance to go home: ", go)

	if go < 751: #they go for home
		print("Going home...")
		outfield = getOutcome()
		print("Outfield throw: ", outfield)
		
		if outfield > 100: 
		#the outfielder did not throw them out
			runScores()
		else:
			print("Out at the plate") 
			#the outfielder did throw them out
			outs += 1
			print("Outfielder ", random.randint(7,9), " made the throw")
	else:
		onThird = 1 
		#the runner did not go home, stays on third

#determines which player made the error, default is outfielder
def printError(outfield = True):
	print("Error")

	if outfield == False:
		player = random.randint(1,6)
	else:
		player = random.randint(7,9)

	print(player, " committed the error")


#simulates an at-bat
while next != 1: #while the game is still going on
	
	#if the home team is batting with the lead in the 9th inning or later, they win
	if inning >= 9 and atBat == team2 and home > away:
		print('The game is over.')
		break

	print("----------------------------------------")
	print(atBat, " are at bat")

	if next == 5: #if the pitcher is removed
		print("**PITCHING CHANGE**")
		if atBat == team1: #if the home team is pitching
			print("End pitches: ", totPitchesHome)
			totPitchesHome = 0 #the new pitcher will now have 0 pitches
			print(team2, " has a new pitcher")
		else: #if the away team is pitching
			print("End pitches: ", totPitchesAway)
			totPitchesAway = 0 #the new pitcher will now have 0 pitches
			print(team1, " has a new pitcher")

	if outs >= 3: #if there are 3 outs
		print("**INNING OVER**")

		#switch sides
		if atBat == team1:
			atBat = team2
		else:
			atBat = team1
			inning += 1
		
			#if the away team is batting with the lead after the 9th inning, they win
			if inning >= 10 and away > home:
				print('The game is over.')
				break

		outs = 0
		onFirst = 0
		onSecond = 0
		onThird = 0
		pitches = 0

		print(team1, ": ", away, " - ", team2, ": ", home)
		print("Inning: ", inning, ", at-bat: ", atBat)

	else: #the inning continues

		#simulate a plate appearance
		outcome = getOutcome()
		print("Outcome: ", outcome)
		pitches = random.randint(1,6)


		if outcome > 0 and outcome < 151: #The batter hits a single
			print("Single")

			if onThird == 1: #if there's a runner on third, a run scores
				runScores()
				onThird = 0 #there's now no one on third

			if onSecond == 1: #if there's a runner on second
				goHome()
				onSecond = 0 #no one is on second anymore

			if onFirst == 1: # if there's a runner at first
				if onThird == 0:		
					goThird = getOutcome()
					print("Chance to go to third: ", goThird)

					if goThird < 501: #they go for third
						outfield = getOutcome()
						print("Outfield throw: ", outfield)

						if outfield > 100: 
						#the outfielder did not throw them out
							onThird = 1
							print("First to third")
						else:
						#the outfielder did throw them out
							print("Out at third")
							outs += 1
							print("Outfielder ", random.randint(7,9), " made the throw")
					else:
					#the runner did not go to third, advances to second
						onSecond = 1
				
				else:
					onSecond = 1 
					#the runner can't go to third, advance to second

			onFirst = 1

		elif outcome > 150 and outcome < 197:
			print("Double")

			if onThird == 1 or onSecond == 1: #if there's runners in scoring position
				runScores(onThird + onSecond)

				#now no one is on second or third
				onThird = 0
				onSecond = 0

			if onFirst == 1:
				goHome()
				onFirst = 0 #no one is on first anymore

			onSecond = 1

		elif outcome > 196 and outcome < 202:
			print("Triple")

			if onThird == 1 or onSecond == 1 or onFirst == 1:
				runScores(onFirst + onSecond + onThird)

			onThird = 1
			onSecond = 0
			onFirst = 0

		elif outcome > 201 and outcome < 228:
			print("Home run")
			runScores(1 + onFirst + onSecond + onThird) #all runners and the batter score
			onFirst = 0
			onSecond = 0
			onThird = 0 #the homer clears the bases

		elif outcome > 227 and outcome < 315:
			print("Walk")
			if pitches < 4:
				pitches = 4
			if onFirst == 1:
				if onSecond == 1:
					if onThird == 1: #the bases were loaded
						runScores()
					else: #there was first and second
						onThird = 1
				else: #there was a runner on first (and maybe third) but not on second
					onSecond = 1
			else: #there was no one on first but maybe on second and third
				onFirst = 1

		elif outcome > 314 and outcome < 324:
			print("Hit by pitch")			

			if onFirst == 1:
				if onSecond == 1:
					if onThird == 1: #the bases were loaded
						runScores()
					else: #there was first and second
						onThird = 1
				else: #there was a runner on first (and maybe third)
					onSecond = 1
			else: #there was no one on first
				onFirst = 1

		elif outcome > 323 and outcome < 506:
			print("Strikeout")
			if pitches < 3:
				pitches = 3
			outs += 1

		elif outcome > 505 and outcome < 751:
			print("Groundout")
			
			if outs == 2:
				error = getOutcome()
				print("Error chance: ", error)

				if error <= 984: #an error was not committed
					outs += 1
				else: #an error was committed
					printError(outfield = False)

					if onFirst == 0:
						if onSecond == 0:
							if onThird == 0: #bases empty
								onFirst = 1 #batter reaches on error
							else: #runner on third
								onFirst = 1 #batter reaches on error
								runScores() #runner on third scores

								onThird = 0 #now there's no one on third anymore
						else: 
							if onThird == 0: #runner on second
								onFirst = 1
								onSecond = 0
								onThird = 1
								#now there's runners at the corners
							else: #runners at second and third
								onFirst = 1
								onSecond = 0
								onThird = 1
								#now there's runners at the corners
								runScores() #the runner previously at third scores

					else:
						if onSecond == 0:
							if onThird == 0: #runner on first
								onFirst = 1
								onSecond = 1
								#now there's first and second
							else: #runners at the corners
								onFirst = 1
								onSecond = 1
								#now there's first and second
								runScores() #the runner previously at third scores
								
								onThird = 0 #now no one is on third
						else:
							if onThird == 0: #runners at first and second
								onFirst = 1
								onSecond = 1
								onThird = 1 #now the bases are loaded
							else: #bases loaded
								onFirst = 1
								onSecond = 1
								onThird = 1 #now the bases are loaded

								runScores() #the runner previously at third scores

			elif onFirst == 0:
				error = getOutcome()
				print("Error chance: ", error)

				if error <= 984: #an error was not committed
					outs += 1
				else: #an error was committed
					printError(outfield = False)
					
					if onSecond == 0:
						if onThird == 0: #bases empty
							onFirst = 1 #batter reaches on error
						else: #runner on third
							onFirst = 1 #batter reaches on error
							runScores() #the runner at third scores		
							onThird = 0 #now there's no one on third anymore
					else: 
						if onThird == 0: #runner on second
							onFirst = 1
							onSecond = 0
							onThird = 1
							#now there's runners at the corners
						else: #runners at second and third
							onFirst = 1
							onSecond = 0
							onThird = 1
							#now there's runners at the corners
							runScores() #the runner previously at third scores

			else:
				doublePlay = getOutcome()
				print("Double play chance: ", doublePlay)
				error = getOutcome()
				print("Error chance: ", error)
				
				if doublePlay > 400 or error > 984: #no double play
					if error <= 984: #an error was not committed
						if onSecond == 1 and onThird == 1: #bases loaded
							base = random.randint(1,4)
							print("Base: ", base)

							if base == 4: #throw home
								print("Out at home")
								outs += 1
								#bases remain loaded

							elif base == 3: #throw to third
								print("Out at third")
								outs += 1
								runScores() #the runner at third scores			
								onThird = 0 #now first and second

							elif base == 2:	#throw to second
								print("Out at second")
								outs += 1
								runScores() #the runner at third scores
								onSecond = 0 #now runners at the corners					

							else: #throw to first
								print("Out at first")
								outs += 1
								runScores() #the runner at third scores
								onFirst = 0 #now runners at second and third

						elif onSecond == 1 and onThird == 0: #first and second
							base = random.randint(1,3)
							print("Base: ", base)

							if base == 3:
								print("Out at third") #throw to third
								outs += 1
								#runners still on first and second

							elif base == 2:	#throw to second
								print("Out at second")
								outs += 1
								onThird = 1
								onSecond = 0 #now runners at the corners

							else: #throw to first
								print("Out at first")
								outs += 1
								onFirst = 0
								onSecond = 1
								onThird = 1 #now runners at second and third

						elif onSecond == 0 and onThird == 1: #runners on the corners
							runScores() #the runner at third scores
							onThird = 0

							base = random.randint(1,2)
							print("Base: ", base)

							if base == 2: #throw to second
								print("Out at second")
								outs += 1

							else: #throw to first
								print("Out at first")
								outs += 1
								onSecond = 1 #now runner at second
								onFirst = 0

						else: #runner at first
							base = random.randint(1,2)
							print("Base: ", base)

							if base == 2: #throw to second
								print("Out at second")
								outs += 1
								#runner still at first

							else: #throw to first
								print("Out at first")
								outs += 1
								onFirst = 0
								onSecond = 1 #now runner at second

					else: #an error was committed
						printError(outfield = False)

						if onSecond == 0:
							if onThird == 0: #runner on first
								onSecond = 1 #batter reaches on error, now first and second
							else: #runners on the corners
								onSecond = 1 #batter reaches on error, now first and second
								runScores() #the runner at third scores		
								onThird = 0 #now there's no one on third anymore
						else: 
							if onThird == 0: #runner on first and second
								onFirst = 1
								onSecond = 1
								onThird = 1
								#runner reaches on error, now there's bases loaded
							else: #bases loaded
								onFirst = 1
								onSecond = 1
								onThird = 1
								#still bases loaded
								runScores() #a runner scores

				else: #there was a double play
					print("Double Play")
					if onSecond == 1 and onThird == 1: #bases loaded
						base = random.randint(2,4)
						print("Base: ", base)

						if base == 4: #throw home
							print("Out at home and first")
							outs += 2
							onFirst = 0 #runners at second and third

						elif base == 3: #throw to third
							print("Out at third and first")
							outs += 2

							if outs != 3: #if there's only 2 outs
								runScores() #the runner at third scores
							
							onFirst = 0
							onThird = 0 #runner at second (if the inning is still going)

						elif base == 2:	#throw to second
							print("Out at second and first")
							outs += 2
							if outs != 3: #if there's only 2 outs
								runScores() #the runner at third scores
							onFirst = 0
							onSecond = 0 #now runner at third (if the inning is still going)				

					elif onSecond == 1 and onThird == 0: #first and second
						base = random.randint(2,3)
						print("Base: ", base)

						if base == 3:
							print("Out at third and first") #throw to third
							outs += 2
							onFirst = 0 #now only runner at second (if inning continues)

						elif base == 2:	#throw to second
							print("Out at second and first")
							outs += 2
							onThird = 1
							onSecond = 0
							onFirst = 0 #now only runner at third (if inning continues)

					elif onSecond == 0 and onThird == 1: #runners on the corners
						print("Out at second and first")
						outs += 2
						if outs != 3: #if there's only 2 outs
							runScores()
						onThird = 0
						onFirst = 0 #bases empty (if inning continues)

					else: #runner at first
						print("Out at second and first")
						outs += 2
						onFirst = 0
						#bases empty (if inning continues)

		elif outcome > 750 and outcome < 951:
			print("Flyout")	
			error = getOutcome()
			print("Error chance: ", error)
			
			if error <= 984: #an error was not committed
				outs += 1
				if outs != 3 and onThird == 1: #runner at third, less than 2 outs
					tryToScore = getOutcome()
					print("Chance to go home: ", tryToScore)

					if tryToScore < 751: #the runner goes home
						print("Going home...")
						outfield = getOutcome()
						print("Outfield throw: ", outfield)
						if outfield >= 101: #runner is safe
							runScores()#runner scores at home
						else: #outfield assist
							print("Out at home")
							outs += 1
							print("Outfielder ", random.randint(7,9), " made the throw")
						onThird = 0 #the runner is no longer on third

						
			else: #an error was committed
				printError()

				if onThird == 1:
					runScores()
					onThird = 0 #the runner scores and now no one is on third
				if onSecond == 1:
					onSecond = 0
					onThird = 1 #the runner moves up to third
				if onFirst == 1:
					onFirst = 0
					onSecond = 1 #the runner moves up to second
				onFirst = 1 #the runner reaches on an error

			

		else:
			print("Infield Fly")
			
			if onFirst == 1 and onSecond == 1 and outs < 2:
				outs += 1
				print("Infield Fly Rule") #infield fly rule, runners stay

			else:
				error = getOutcome()
				print("Error chance: ", error)
				
				if error <= 984: #an error was not committed
					outs += 1 #runners stay where they are

				else: #an error was committed
					printError(outfield = False)

					if onThird == 1:
						runScores()
						onThird = 0 #the runner scores and now no one is on third
					if onSecond == 1:
						onSecond = 0
						onThird = 1 #the runner moves up to third
					if onFirst == 1:
						onFirst = 0
						onSecond = 1 #the runner moves up to second
					onFirst = 1 #the runner reaches on an error	
	

	print("Pitches thrown: ", pitches)
	if atBat == team1:
		totPitchesHome += pitches
		print("Total pitches: ", totPitchesHome)
	else:
		totPitchesAway += pitches
		print("Total pitches: ", totPitchesAway)



	if onFirst == 1:
		if onSecond == 1:
			if onThird == 1:
				print("Bases loaded")
			else:
				print("First and second")
		else:
			if onThird == 1:
				print("Runners on the corners")
				steal = getOutcome()
				print("Steal chance: ", steal)

				if steal <= 48: #runner successfully steals
					onFirst = 0
					onSecond = 1
					print("Stolen base, second and third")
				
				elif steal > 48 and steal < 66: #runner caught stealing
					onFirst = 0
					outs += 1
					print("Caught stealing, runner at third")

			else:
				print("Runner at first")
				steal = getOutcome()
				print("Steal chance: ", steal)

				if steal <= 48: #runner successfully steals
					onFirst = 0
					onSecond = 1
					print("Stolen base, runner at second")
				
				elif steal > 48 and steal < 66: #runner caught stealing
					onFirst = 0
					outs += 1
					print("Caught stealing, bases empty")				

	else:
		if onSecond == 1:
			if onThird == 1:
				print("Second and third")
			else:
				print("Runner at second")
				steal = getOutcome()
				print("Steal chance: ", steal)

				if steal <= 48: #runner successfully steals
					onSecond = 0
					onThird = 1
					print("Stolen base, runner at third")
				
				elif steal > 48 and steal < 66: #runner caught stealing
					onSecond = 0
					outs += 1
					print("Caught stealing, bases empty")
		else:
			if onThird == 1:
				print("Runner at third")
			else:
				print("Bases empty")

	print("There are ", outs, " outs")

	#asks the user to continue the game, change pitchers, or quit the game early
	while True:
		try:
			next = int(input('Next batter? Enter 5 to change the pitcher, 1 if the game is over, or 0 to continue'))

			#the user must input a 0, 1, or 5 to continue
			if next == 0 or next == 1 or next == 5:
				break
			print('Invalid Input') 

		#the user must input a 0, 1, or 5 to continue	
		except ValueError:
			print('Incorrect input. Please enter 5 to change the pitcher, 1 if the game is over, or 0 to continue') 
	

print(team1, ": ", away, " - ", team2, ": ", home) #print the score
if away > home:
	print(team1, " wins")
else:
	print(team2, " wins")

#print the number of pitches for the pitchers that finished the game
print("Current ", team1, " pitcher has ", totPitchesAway, " pitches")
print("Current ", team2, " pitcher has ", totPitchesHome, " pitches")