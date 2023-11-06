#just gonna setup the environments and printing functions since I dont understand shit

import numpy as np
 
BOARD_ROWS = 5
BOARD_COLS = 5
PICK_UP_STATE = [(0,0), (1,4), (3,4), (4,0)]
RESTRICTED_STATE = [(2,2), (2,3), (2,4)]

class State:
    def __init__(self):
        self.rows = BOARD_ROWS
        self.cols = BOARD_COLS
        self.pick_up_states = PICK_UP_STATE
        self.restricted_states = RESTRICTED_STATE
     
class Car:
    def __init__(self):
        self.position = (1,1)

    def nxtPosition(self, action):
        if action == "up":
           nxtState = (self.position[0]-1, self.position[1])
        elif action == "down":
                nxtState = (self.position[0] + 1, self.position[1])
        elif action == "left":
                nxtState = (self.position[0], self.position[1] - 1)
        else:
                nxtState = (self.position[0], self.position[1] + 1)

        if (nxtState[0] >= 0) and (nxtState[0] <= (BOARD_ROWS-1)):
            if (nxtState[1] >= 0) and (nxtState[1] <= (BOARD_COLS-1)):
                self.position = nxtState 
            
        return self.position

class Customer:
    def __init__(self, type):
        self.type = type
        if(type == 1):
            self.reward = 30
        else:
            self.reward = 20
        
class Agent:
    def __init__(self):
        self.state = State()
        self.actions = ["up", "down", "left", "right"]
        self.State = State()
        self.lr = 0.2
        self.exp_rate = 0.3
        self.u_value = {}
        for a in range(self.state.rows):
            for b in range(self.state.cols):
                self.u_value[(a, b)] = {}
                for i in self.actions:
                    self.u_value[(a, b)][i] = 0
    
    def chooseAction(self):
       pass

    def takeAction(self, action):
        pass

    def play(self, rounds):
       pass
    
    def showAllUvalues(self):
        for i in range(0, BOARD_ROWS):
            print('----------------------------------')
            for j in range(0, BOARD_COLS):
                print("For", i , j)
                print(self.u_value[(i,j)])
                print()
            print('----------------------------------')

    def showTrace(self):
        for i in range(0, BOARD_ROWS):
            out = '| '
            out2 = '| '
            print('--------------------------')
            for j in range(0, BOARD_COLS):
                dict = self.u_value[(i,j)]
                max_action = max(dict, key=dict.get)
                out += str(max_action) + ' | '
                out2 += str(dict[max_action]) + '  | '
            print(out)
            print(out2)
            # print('----------------------------------')


        for i in range(0, BOARD_ROWS):
            print('----------------------------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                out += str(self.state_values[(i, j)]).ljust(6) + ' | '
            print(out)
        print('----------------------------------')

if __name__ == "__main__":
    ag = Agent()
    ag.showTrace()
    # print(ag.showValues())