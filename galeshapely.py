import numpy as np
import pandas as pd
import random
import time

'''
stable_match(k,n,H,S,Hi,Si)
    returns tuple (matches,rounds)
matches - is a list, where the indeices are hospitals and values are the matched students. 
rounds  - is a integer denoting the number of rounds needed to find stable match of all the hospitals
'''
def stable_match(k,n,H,S,Hi,Si):
    #All hospitals are unmatched at first
    unmatchedH = list(range(n))
    #No hospital selected any student, 
    #neither the student selected any hospitals, 
    #so an array of None
    hospital = [None]*n
    student = [None] *n
    #pointer to next proposal, it helps to keep track of the students
    #that a hospital will propose next
    #at the beginning,hospital's next proposal
    #would be to the 0th (first) preference in his ranking
    nextStudentPointers = [0]*n
    iteration = 0
    while unmatchedH:
        h = unmatchedH[0] #selecting an unmatched hospital
        hranking = H[Hi[h]] #assigning its ranking list from input
        s = hranking[nextStudentPointers[h]] #getting the student that is next on h's ranking
        sranking = S[Si[s]] #storing student S's ranking
        # Find if any match already exists, might be None
        sCurrentMatch = student[s]
        iteration = iteration +1
        #Hospital proposes to the student
        if sCurrentMatch==None:
            # No current match case
            # store the match
            student[s] = h
            hospital[h]= s
            # increase student pointer
            nextStudentPointers[h] = nextStudentPointers[h]+1
            # remove the Hospital from the unmatched list
            unmatchedH.pop(0)
        else:
            # a match already exists
            #check the index in the pref list for the student
            #if the student likes this hospital more than the
            #present match
            currentMatchIndex = sranking.index(sCurrentMatch)
            hIndex= sranking.index(h)
            # s accepts the proposal if the currentMatch index 
            # is bigger than hIndex (as h is more preferable then)
            if  hIndex<currentMatchIndex:
                #s accepts h
                student[s] = h
                hospital[h] = s
                nextStudentPointers[h] = nextStudentPointers[h]+1
                unmatchedH.pop(0)
                # add the current match to the unmatched list
                unmatchedH.insert(0,sCurrentMatch)
                
            else:
                #s rejects h
                nextStudentPointers[h] = nextStudentPointers[h]+1
    #print("{} rounds used".format(iteration))
    return (hospital,iteration)
                         
    
#Generating random data for testing the implementation

k=50
n=70
#initializing H randomly
H = [[0]*n]*k  # [[value]*rows]*columns
for i in range(k):
    H[i] = random.sample(range(n), n)

#initializing S randomly
S = [[0]*n]*k  # [[value]*rows]*columns
for i in range(k):
    S[i] = random.sample(range(n),n)

#initializing Hi & Si randomly, to determine a row of H & S 2D array to be the pref list
Hi= random.choices(range(k),k=n) #second parameter k is the param name of random.choices()
Si= random.choices(range(k),k=n)

## testing the stable_match() function
h,round = stable_match(k,n,H,S,Hi,Si)
print("Hospital    Student")
for hospital, student in enumerate(h):
    print("    "+str(hospital)+"        "+str(student))
print(str(round) + " Rounds occured")
