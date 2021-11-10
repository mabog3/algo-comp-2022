import numpy as np
from typing import List, Tuple

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """

    #change scores of incompatible pairs to be 0 
    n = len(scores) 
    for i in range(n - 1):
        for j in range(i + 1, n):
            if (gender_pref[i] == "Women" and gender_id[j] != "Female") or (gender_pref[i] == "Men" and gender_id[j] != "Male"):
                scores[i][j] = 0 
            if (gender_pref[j] == "Women" and gender_id[i] != "Female") or (gender_pref[j] == "Men" and gender_id[i] != "Male"):
                scores[j][i] = 0


    matches = [()]

    middle = int(n / 2) #first half will be proposers, second half will be recievers 

    ranklist = [None]*n
    for person in range(n): # get preferences from scores 
        scorelist = scores[person]
        preferences = [] 
        for j in range(n):
            # if j != person: 
            preferences.append([j, scorelist[j]]) #pairs score with the person who scored it 
        sorted(preferences, key=lambda l:l[1], reverse=True) 
        for k in range(len(preferences)):
            preferences[k] = preferences[k][0] #just leaves the people in the ranking
        ranklist[person] = preferences

    unmatched_proposers = []
    reciever_matches = [None]*(middle)

    for proposer in range(middle):
        unmatched_proposers.append(proposer)

    while unmatched_proposers != []:
        prop = unmatched_proposers.pop()
        matched = False
        for reciever in ranklist[prop]:
            if not matched: 
                if reciever_matches[reciever - middle] == None:
                    reciever_matches[reciever - middle] = prop 
                    matched = True
                else: 
                    if ranklist[reciever][prop] > ranklist[reciever][reciever_matches[reciever - middle]]:
                        unmatched_proposers.append(reciever_matches[reciever - middle])
                        reciever_matches[reciever - middle] = prop 
                        matched = True
        if not matched:
            unmatched_proposers.append(prop)

    for i in range(len(reciever_matches)):
        matches.append((reciever_matches[i], i))
        
    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
