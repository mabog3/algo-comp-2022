#!usr/bin/env python3
import json
import sys
import os
import math 
import statistics

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses

def calculate_stats():
    numUsers = len(users)
    numQuestions = len(users[0].responses)
    responsesPer = []
    

    for i in range(numQuestions):
        resp = []
        for j in range(numUsers): 
            resp.append(users[j].responses[i])
        responsesPer.append(resp)
    responseProportions = []

    for i in range(numQuestions): #gives the proportion of responses each answer choice was, for each question
         #number of responses to question i should equal num. of users
        proportions = [0]*numUsers 
        numEachOption = [0]*(max(responsesPer[i]) + 1)# number of answer choices
        for response in responsesPer[i]:
            numEachOption[response] += 1 #response i => numeachOption[i] incremented; start at 0 
        for j in range(len(numEachOption)):
            proportions[j] = numEachOption[j]/numUsers
        responseProportions.append(proportions)
    
    # for i in range(numQuestions):
    #     means.append(sum(responsesPer[i])/numUsers) # mean response to q i 
    #     stdevs.append(statistics.stdev(responsesPer[i])) #st deviation of responses to q i
    #     modes.append(statistics.mode(responsesPer[i]))
        

    return responseProportions
        

# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    if not ((user1.gender in user2.preferences) and (user2.gender in user1.preferences)):
        return 0 #incompatible sexualities
    numqs = len(user1.responses)
    answerCompatability = 0 
    for i in range(numqs): 
        if user1.responses[i] == user2.responses[i]:
            answerCompatability += 1/(1 + stats[i][user1.responses[i]]) #at most 1 
        else: 
            answerCompatability = max(0,answerCompatability - (1/numqs)*(1/(1 + math.sqrt(stats[i][user1.responses[i]] * stats[i][user2.responses[i]]))))

    
    diff = abs(user1.grad_year - user2.grad_year)
    if diff == 0: 
        answerCompatability += 1 #same as 1 identical answers with high weight
    elif diff == 1:
        answerCompatability += .5 #same as 1 identical answer with average weight
    
    answerCompatability = answerCompatability / (numqs + 1) #max compat. is numqs + 1 (with grade boost); normalize

    
    return answerCompatability


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    stats = calculate_stats() #placed in main to minimize runtime contribution 
    print(stats)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
