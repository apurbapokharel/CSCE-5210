import random as random
import numpy as np

BOARD_ROWS = 5
BOARD_COLS = 5
PICK_UP_STATE = [(0,1), (0,3), (4,0), (4,4)]
RESTRICTED_STATE = [(1,2)]
GAMMA = 0.9

class State:
    def __init__(self):
        self.rows = BOARD_ROWS
        self.cols = BOARD_COLS
        self.pick_up_states = PICK_UP_STATE
        self.restricted_states = RESTRICTED_STATE
     
class Car:
    def __init__(self, ran = 0):
        if ran == 0:
            self.position = (3,1)
        else:
            while 1:
                random_row = random.randint(0,BOARD_ROWS - 1)
                random_cols = random.randint(0, BOARD_COLS - 1)
                if (random_row, random_cols) != RESTRICTED_STATE[0]:
                    self.position = (random_row, random_cols)
                    break

    def nxtPosition(self, action, position):
        if action == "up":
           nxtState = (position[0] - 1, position[1])
        elif action == "down":
            nxtState = (position[0] + 1, position[1])
        elif action == "left":
            nxtState = (position[0], position[1] - 1)
        else:
            nxtState = (position[0], position[1] + 1)

        if (nxtState[0] >= 0) and (nxtState[0] <= (BOARD_ROWS-1)):
            if (nxtState[1] >= 0) and (nxtState[1] <= (BOARD_COLS-1)):
                return nxtState
            
        return position

class Customer:
    def __init__(self, ctype, pick_up_name):
        self.type = ctype
        if(ctype == 1):
            self.reward_multiplier = 1.5
        else:
            self.reward_multiplier = 1
        self.pick_up_point = self.getPickUpCoordinate(pick_up_name)

    def getPickUpCoordinate(self, pick_up_name):
        if pick_up_name == "A":
            return (0,1)
        elif pick_up_name == "B":
            return (0,3)
        elif pick_up_name == "C":
            return (4,0)
        else:
            return (4,4)
        
class Agent:
    def __init__(self):
        self.state = State()
        self.actions = ["up", "down", "left", "right"]
        self.State = State()
        self.u_value = {}
        self.reward_state = []
        self.difference_factor = 0.01 #this is Episilon
        self.transition_probability= {}

    def getPickUpName(self, coordinate):
        if coordinate == 0:
            return "A"
        elif coordinate == 1:
            return "B"
        elif coordinate == 2:
            return "C"
        else:
            return "D"
        
    def updateReward(self, type, pick_up_name):
        for a in range(self.state.rows):
            for b in range(self.state.cols):
                self.u_value[(a, b)] = 0

        for a in RESTRICTED_STATE:
                self.u_value[a] = -10

        coordinate = self.customer_one.getPickUpCoordinate(pick_up_name)
        if(type == 1):
            self.u_value[coordinate] = 30
        else:
            self.u_value[coordinate] = 20

        self.reward_state.append(coordinate)

    def updateRewardTwo(self, type_one, pick_up_name_one, type_two, pick_up_name_two):
        for a in range(self.state.rows):
            for b in range(self.state.cols):
                self.u_value[(a, b)] = 0

        for a in RESTRICTED_STATE:
                self.u_value[a] = -10

        coordinate_one = self.customer_one.getPickUpCoordinate(pick_up_name_one)
        coordinate_two = self.customer_two.getPickUpCoordinate(pick_up_name_two)

        if(type_one == 1):
            self.u_value[coordinate_one] = 30
        else:
            self.u_value[coordinate_one] = 20

        if(type_two == 1):
            self.u_value[coordinate_two] = 30
        else:
            self.u_value[coordinate_two] = 20

        self.reward_state.append(coordinate_one)
        self.reward_state.append(coordinate_two)
        
    def simulateRequirementOne(self):
        self.customer_one = Customer(0, "A")
        self.updateReward(0, "A")
        self.car = Car()
        self.valueIteration(k = 100)
    
    def simulateRequirementTwo(self):
        self.customer_one = Customer(1, "B")
        self.updateReward(1, "B")
        self.car = Car()
        self.valueIteration(k = 100)

    def simulateRequirementThree(self):
        self.customer_one = Customer(0, "A")
        self.customer_two = Customer(1, "B")
        self.updateRewardTwo(0, "A", 1, "B")
        self.car = Car()
        self.valueIteration(k = 100)

    def simulateRequirementFour(self):
        k = 0
        count = 0
        premium_selection = 0
        while k<1000:
            k +=1
            any_one_premium = 0
            # Generate a random number between 0 and 3 
            # Such that each number maps to a pickup point(0->A 1->B 2->C 3->D)
            pick_up_index_one = random.randint(0,4)
            pick_up_name_one = self.getPickUpName(pick_up_index_one)
            
            #generate 2nd request only 60% of the time
            pick_up_index_two = -1
            probability = random.randint(1,10)
            if probability <=6:
                while(1):
                    pick_up_index_two = random.randint(0,4)
                    pick_up_name_two = self.getPickUpName(pick_up_index_two)
                    if pick_up_name_one != pick_up_name_two:
                        break
            else:
                # print("just one")
                self.customer_one = Customer(0, pick_up_name_one)
                self.updateReward(0, pick_up_name_one)
            
            # If two request are received one of these is a premium customer 30% of the time
            if pick_up_index_two != -1:
                probability = random.randint(1,10)
                if probability <=3:
                    pp = random.randint(1,2)
                    any_one_premium = 1
                    # print("one premium")
                    if pp == 1:
                        # Customer 1 is premium
                        self.customer_one = Customer(1, pick_up_name_one)
                        self.customer_two = Customer(0, pick_up_name_two)
                        self.updateRewardTwo(1, pick_up_name_one, 0, pick_up_name_two)
                    else:
                        # Customer 2 is premium
                        self.customer_one = Customer(0, pick_up_name_one)
                        self.customer_two = Customer(1, pick_up_name_two)
                        self.updateRewardTwo(0, pick_up_name_one, 1, pick_up_name_two)
                else:
                    # print("two regular")
                    self.customer_one = Customer(0, pick_up_name_one)
                    self.customer_two = Customer(0, pick_up_name_two)
                    self.updateRewardTwo(0, pick_up_name_one, 0, pick_up_name_two)
        
            # Generate car in random position
            self.car = Car(ran=1)
            # Run value iteration
            self.valueIteration(k = 100)

            # Calculate the times agent prefered premium customer over regular ones
            if any_one_premium == 1:
                count += 1
                customer_one_coordinate = self.customer_one.pick_up_point
                customer_two_coordinate = self.customer_two.pick_up_point
                car_coordinate = self.car.position

                if self.customer_one.type == 1:
                    distance_to_premium = self.getDistances(customer_one_coordinate, car_coordinate)
                    distance_to_regular = self.getDistances(customer_two_coordinate, car_coordinate)
                else:
                    distance_to_regular = self.getDistances(customer_one_coordinate, car_coordinate)
                    distance_to_premium = self.getDistances(customer_two_coordinate, car_coordinate)

                # print("Distance to pre", distance_to_premium)
                # print("Distnace to reg", distance_to_regular)
                if distance_to_premium <= distance_to_regular:
                    premium_selection += 1
                
            # print("premium_selection", premium_selection)
        print("There was a premium and a regular customer generated ", count, " times")
        print("The fraction of selction of premium over regular was", premium_selection, " / ", count, ", ", premium_selection/count)

    def getDistances(self, customer_pickup, car_origin):
        row_dist = abs(customer_pickup[0] - car_origin[0])
        col_distance = abs(customer_pickup[1] - car_origin[1])
        return row_dist + col_distance
       
    def getStateProbability(self, prev_coordinate, next_coordinate):
        for a in self.reward_state:
            if a == next_coordinate:
                return 0.9
            elif prev_coordinate == next_coordinate:
                return 0
            else:
                return 0.8
        
    def getOtherStateProbability(self, original_coordinate, next_coordinate_one, next_coordinate_two, probability):
        if original_coordinate == next_coordinate_one:
            if original_coordinate != next_coordinate_two:
                #p1 = 0 , p2 != 0
                return (0, 1-probability)
        else:
            if original_coordinate == next_coordinate_two:
                #p1 != 0, p2 = 0
                return (1-probability, 0)
            else:
                #p1 != 0, p2 != 0
                a = (1-probability)/2
                return (a,a)

    
    def isReward(self, coordinate):
        for a in self.reward_state:
            if a == coordinate:
                return True
            
    def isRestricted(self, coordinate):
        for a in RESTRICTED_STATE:
            if a == coordinate:
                return True  
            
    def getEmptyValue(self):
        new_uvalue = {}
        for i in range(0,BOARD_ROWS):
            for j in range(0, BOARD_COLS):
                new_uvalue[(i, j)] = 0

        for a in self.reward_state:
            prev_value = self.u_value[a]
            new_uvalue[a] = prev_value

        return new_uvalue

    def valueIteration(self, k):
        while(k!=0):
            k -=1
            end_loop = True
            # print("iteration number = ", k)
            update_uvalue = self.getEmptyValue()
            for i in range(0,BOARD_ROWS):
                for j in range(0, BOARD_COLS):
                    coordinate = (i,j)
                    if self.isReward(coordinate) or self.isRestricted(coordinate):
                        continue
                    value_array = []
                    for a in self.actions:
                        if a=="up" or a=="down":
                            if a=="up":
                                #goup
                                mcoordinate = self.calculateCordinate(coordinate, "up")
                                mprobability = self.getStateProbability(coordinate, mcoordinate)
                            else:
                                #godown
                                mcoordinate = self.calculateCordinate(coordinate, "down")
                                mprobability = self.getStateProbability(coordinate, mcoordinate)

                            left_coordinate = self.calculateCordinate(coordinate, "left")
                            right_coordinate = self.calculateCordinate(coordinate, "right")
                            other_probability = self.getOtherStateProbability(coordinate, left_coordinate, right_coordinate, mprobability)
                            # print('other prob', mprobability, other_probability)
                            #do the calculation
                            value = mprobability * self.u_value[mcoordinate] + other_probability[0] * self.u_value[left_coordinate] +  other_probability[1] * self.u_value[right_coordinate]
                        else:
                            if a=="left":
                                #goleft
                                mcoordinate = self.calculateCordinate(coordinate, "left")
                                mprobability = self.getStateProbability(coordinate, mcoordinate)
                            else:
                                #goright
                                mcoordinate = self.calculateCordinate(coordinate, "right")
                                mprobability = self.getStateProbability(coordinate, mcoordinate)

                            up_coordinate = self.calculateCordinate(coordinate, "up")
                            down_coordinate = self.calculateCordinate(coordinate, "down")
                            other_probability = self.getOtherStateProbability(coordinate, up_coordinate, down_coordinate, mprobability)

                            #do the calculation
                            value = mprobability * self.u_value[mcoordinate] + other_probability[0] * self.u_value[up_coordinate] +  other_probability[1] * self.u_value[down_coordinate]

                        value_array.append(value)
                    #get the max value array and update the u value
                    max_value = max(value_array)
                    value = -0.1 + GAMMA * max_value
                    old_value = self.u_value[coordinate]
                    if abs(old_value - value) > self.difference_factor:
                        end_loop = False
                    update_uvalue[coordinate] = value

            self.u_value = update_uvalue
            if end_loop:
                break

                            
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
            total = 8
            print('---------------------------------------------------')
            for j in range(0, BOARD_COLS):
                if (i,j) == self.car.position:
                    value = 'Car'
                else:
                    value = round(self.u_value[(i,j)],2)
                    lenn = 0

                if value == 'Car':
                    out+= value
                    lenn = 3
                elif value == 0:
                    out+= '0'
                    lenn = 1
                elif value<0:
                    out+= str(value)
                    lenn = len(str(value))
                else:
                    out += str(value)
                    lenn = len(str(value))
                
                rem = total - lenn
                while(rem !=0):
                    out+= ' '
                    rem -=1
                out += '| '
            print(out)

if __name__ == "__main__":
    ag = Agent()
    ag.simulateRequirementOne()
    # ag.showTrace()
    del ag
    print("--------")
    ag = Agent()
    ag.simulateRequirementTwo()
    # ag.showTrace()
    del ag
    print("--------")
    ag = Agent()
    ag.simulateRequirementThree()
    # ag.showTrace()
    del ag
    print("--------")
    ag = Agent()
    ag.simulateRequirementFour()
    # ag.showTrace()
