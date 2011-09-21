#!/usr/bin/python

import sys
from optparse import OptionParser


def CalculateQ(Q_db, V_db, alpha, beta, state, action, nextstate, reward):
    # Calculate the max
    q_max = 0.0
    for key in Q_db[state].keys():
        if Q_db[state][key] > q_max:
            q_max = Q_db[state][key]
    V_db[state] = q_max
    
    if not V_db.has_key(nextstate):
        V_db[nextstate] = 0.5
    
    return (1-alpha)*(Q_db[state][action]) + alpha*(reward + beta*V_db[nextstate])
    pass



def AddOptions(parser):
    parser.add_option("-a", "--alpha", dest="alpha", help="Alpha to be used in calculations")
    parser.add_option("-b", "--beta", dest="beta", help="Beta to be used in calculations")
    parser.add_option("-r", "--reward", dest="reward", help="Reward for the action")
    parser.add_option("-s", "--state", dest="state", help="State currently")
    parser.add_option("-n", "--nextstate", dest="nextstate", help="Next State")
    parser.add_option("-t", "--action", dest="action", help="Action taken")
    parser.add_option("-p", "--print", dest="print_qs", help="Print the Q values so far", default=False, action="store_true")
    parser.add_option("-d", "--dbfile", dest="dbfile", help="Where to store dbfile with previous information", default="qsdb.csv")
    parser.add_option("-c", "--csvfile", dest="csvfile", help="Whether to output a csv file when printing", default=False, action="store_true")

def main():

    # Q dictionary
    Q = {}
    V = {}
    
    # Read options
    parser = OptionParser()
    AddOptions(parser)
    (options, args) = parser.parse_args()
    
    # Add Q to csv file
    if not options.print_qs:
        f = open(options.dbfile, 'a')
        f.write(options.state + "," + options.action + "," + options.nextstate + "," + options.reward + "\n")
        f.close()

    # Read in the csv file
    f = open(options.dbfile, 'r')
    for line in f.readlines():
        line = line.strip()
        (state, action, nextstate, reward) = line.split(",")
        if not Q.has_key(state):
            Q[state] = {}
        if not Q.has_key(nextstate):
            Q[nextstate] = {}
        if not Q[state].has_key(action):
            Q[state][action] = 0.5
            
        Q[state][action] = CalculateQ(Q, V, float(options.alpha), float(options.beta), state, action, nextstate, float(reward))
       
    
    if options.print_qs == True:
        for state_key in Q.keys():
            for action_key in Q[state_key].keys():
                if options.csvfile:
                    print state_key + "," + action_key + "," + str(Q[state_key][action_key])
                else:
                    print state_key + " " + action_key + " " + str(Q[state_key][action_key])
    else:
        print "New Q for state: " + options.state + ", action: " + options.action
        print Q[options.state][options.action]
    


if __name__ == "__main__":
    main()



