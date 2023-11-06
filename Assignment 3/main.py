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

    def nxtPosition(self, action, position):
        if action == "up":
           nxtState = (position[0], position[1]+1)
        elif action == "down":
            nxtState = (position[0], position[1]-1)
        elif action == "left":
            nxtState = (position[0]-1, position[1])
        else:
            nxtState = (position[0]+1, position[1])

        if (nxtState[0] >= 0) and (nxtState[0] <= (BOARD_ROWS-1)):
            if (nxtState[1] >= 0) and (nxtState[1] <= (BOARD_COLS-1)):
                return nxtState

        return position

class Customer:
    def __init__(self, ctype, pick_up_point):
        self.type = ctype
        if(ctype == 1):
            self.reward = 30
        else:
            self.reward = 20
        self.pick_up_point = self.getPickUpCoordinate(pick_up_point)

    def getPickUpCoordinate(self, pick_up_point):
        if pick_up_point == "A":
            return (0,4)
        elif pick_up_point == "B":
            return (3,4)
        elif pick_up_point == "C":
            return (0,0)
        else:
            return (0,4)
        
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

    def simulateRequirementOne(self):
        self.customer = Customer(0, "A")
        self.car = Car()
        self.getStateProbability()
        self.valueIteration(k = 10)
    
    def getStateProbability(self):
        pass
    
    def valueIteration(self, k):
        while(k!=0):
            print("k")
            k -=1
            for i in range(0,BOARD_ROWS):
                for j in range(0, BOARD_COLS):
                    coordinate = (i,j)
                    for a in self.actions:
                        if a=="up" or a=="down":
                            if a=="up":
                                #goup
                                coordinate = self.calculateCordinate(coordinate, "up")
                            else:
                                #godown
                                coordinate = self.calculateCordinate(coordinate, "down")

                            left_coordinate = self.calculateCordinate(coordinate, "left")
                            right_coordinate = self.calculateCordinate(coordinate, "right")

                        else:
                            if a=="left":
                                #goleft
                                coordinate = self.calculateCordinate(coordinate, "left")
                            else:
                                #goright
                                coordinate = self.calculateCordinate(coordinate, "right")

                            up_coordinate = self.calculateCordinate(coordinate, "up")
                            down_coordinate = self.calculateCordinate(coordinate, "down")
                            
    def calculateCordinate(self, position, action):
        return self.car.nxtPosition(action, position)

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

if __name__ == "__main__":
    ag = Agent()
    ag.simulateRequirementOne()
    # ag.showTrace()
    # print(ag.showValues())