"""
#Author: Paul Gentemann
#Date: Approximately 7/15/11
#Working Title: State Capital Tester
This is a program designed to test your US State geographical trivia, with options for listing alphabetically or randomly the names of the states/names of capitals of states/official state abbreviations. There is also a tracking mechanism to see how many you got right, and how many you got wrong. 
At this point, there are no options to change the number of allowed incorrect guesses, or to toggle hints. Mostly, this was because I didn't want to bother with setting up another menu.
"""

import random, sys

states = []  					        #make list of states
cities = []					            #make list of capital cities
codes = []					            #make list of state abbreviations
combo = []

with open('states.txt', 'r') as f: 		#open info file to read
    for i in range(50):      		    #for each state, read a line of info		
        nextline = f.readline()         #and add the proper info to each list 
        statelist = nextline.split('  ')
        state = statelist[0].capitalize()#format the text to be legible
        states.append(state)

        codes.append(statelist[1])

        cap = statelist[2].rstrip().capitalize() #get rid of \n and capitalize
        cities.append(cap)
        combo.append([state, cap, statelist[1]])

print('Welcome to your humble State Capital memorization tester. Please select one of the following options.\n')

def menu(thing):                        #reusable menu template
    print('Test knowledge (or ENTER to quit):')
    for i in range(1, len(thing)+1):
        print('%d. %s.' % (i, thing[i-1]))


def option(thing):                      #prompt to get a numeric input from user
    selected = False                    #prime the loop
    while not selected:
        user = input("> ")		    #input choice of test
        try:
            user = int(user)	        #make sure it is a number
        except ValueError:		        #if it isn't, it will loop around with a warning
            pass
        if not user: sys.exit('goodbye')#no input quits immediately
        elif 0 < user < len(thing) + 1: #return if user entered a valid option
            return user - 1             #this is the value we care about
        else:
            print("That is not a valid choice, please try again.")


subject = ['of States', 'of Capitals', 'of State Codes'] #list of possible quizzes
test_by = ['In Random Order', 'Alphabetically By State', 'Go Back'] #how to go about testing

link = dict(list(zip(subject, [states, cities, codes])))

first_choice, second_choice = 0, len(test_by) #prime the loop to navigate the menus

while second_choice == len(test_by):    #if the person has selected go back, keep looping
    menu(subject)                       #first menu screen
    first_choice = option(subject)      #display choices and remember selection
    menu(test_by)                       #second menu screen
    second_choice = option(test_by)     #display choices and remember selection

#By this point, we should have integers pointing to one of the testing subjects, and one of the listed methods of testing. Anything else will be caught in the while loop or the user will have quit. To troubleshoot: print first_choice, second_choice

category = first_choice                 #shorthand it: the first choice picks the category
incorrects, corrects = 0, 0             #let's keep track of the guesses!

print('\nLet\'s begin, shall we?')

def comparate(answer, hint):
    global corrects, incorrects         #access the global variables to write to
    guess = input('> ')             #prompt for input
    ttl = 1                             #track total guesses
    same = answer.lower() == guess.strip().lower() #see if guess matches answer (ignoring case or extra spaces at ends)

    while not same:                     #the guessing loop        
        if ttl == 1:                    #first response to wrongness
            print('Sorry. Try again.\n')  
        elif ttl == 2:                  #giving a hint
            print('Here\'s a hint: ', hint)
        elif ttl == 3:                  #give up and move on
            print('Let\'s move on, shall we? The answer was: %r' % answer)
            incorrects += ttl
            break
        guess = input('> ')         #prompt for input
        same = answer.lower() == guess.strip().lower() #update same
        ttl += 1                        #Troubleshooter:  print 'ttl = ', ttl 

    if same == True:
        print('That is correct')         #give them a cookie, then update trackers
        corrects += 1
        incorrects += ttl - 1
        #print 'correct so far: ', corrects, '\nincorrects so far: ', incorrects
    return

if second_choice == 0:                  #for the random order testing method
    print('   ')
    random.shuffle(combo)
    for i in range(50):
        ans = combo[i].pop(first_choice)
        hint = random.randint(0, 1)  
        prompt = 1 - hint
        print('%d States left. %r' % ((50 - i), combo[i][prompt]))
        comparate(ans, combo[i][hint])


if second_choice == 1:                  #for the alphabetical test
    print('Going alphabetically by state, type in your answer. If you need help, a hint shall be offered. Ready? Go!\n\n')
    ans = link[subject[category]] 
    print(len(ans))
    for i in range(50):     #starting with alabama and ending with wyoming
        print('States left:  %d' % (50 - i))
        if first_choice == 2:
            comparate(ans[i], 'the state capital is %r' % cities[i])
        else: comparate(ans[i], 'it starts with %r' % ans[i][0:2]) #go to the comparator function
