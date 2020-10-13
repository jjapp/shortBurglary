from mesa import Agent
import math
import random
import numpy as np


class House(Agent):

    def __init__(self, unique_id, model, attractiveness, x_point, y_point, delta, omega, theta, mu):
        super().__init__(unique_id, model)
        self.attractiveness = attractiveness
        self.x_point = x_point
        self.y_point = y_point
        self.delta = delta
        self.omega = omega
        self.theta = theta
        self.mu = mu
        self.crime_events = 0
        self.crime_list = []
        self.beta = 0
        self.att_t = self.attractiveness + self.beta
        self.p_s = 1 - math.exp(-self.att_t)

    def burgle(self):
        self.crime_events = self.crime_events + 1

    def update_beta(self):
        neighbors = self.model.grid.get_neighbors(pos=(self.x_point, self.y_point),
                                                  moore=True, include_center=False, radius=1)
        b_n = 0
        for i in neighbors:
            if isinstance(i, House):
                b_n = b_n + i.beta
        self.beta = ((1 - self.mu) * self.beta + (self.mu / (len(neighbors)) * b_n) * (1 - self.omega) * (
            self.delta)) + self.theta * self.crime_events

    def update_att(self):
        self.att_t = self.beta + self.attractiveness

    def update_p_s(self):
        self.p_s = 1 - np.exp(-self.att_t * self.delta)

    def update_crime_list(self):
        self.crime_list.insert(0, self.crime_events)
        # check if length is longer than delta
        if len(self.crime_list) > self.delta:
            self.crime_list.pop()
        self.crime_events = 0

    def step(self):
        self.update_beta()
        self.update_att()
        self.update_p_s()
        self.update_crime_list()


class Criminal(Agent):
    def __init__(self, unique_id, model, width, height):
        super().__init__(unique_id, model)
        self.x_point = random.randint(0, width-1)
        self.y_point = random.randint(0, height-1)
        self.decision = 0  # 0 means move, 1 means burgle

    def burgle_decision(self):
        loc_contents = self.model.grid.get_cell_list_contents([(self.x_point, self.y_point)])

        for i in loc_contents:
            if isinstance(i, House):
                p = i.p_s
                y = random.random()
                if y < p:
                    self.decision = 1  # commit burglary at percent p
                else:
                    self.decision = 0  # if you don't burgle you move

    def move(self):
        neighbors = self.model.grid.get_neighbors(pos=(self.x_point, self.y_point), moore=True,
                                                  include_center=False, radius=1)
        # calculate sum of probabilities
        a_t_sum = 0
        for i in neighbors:
            if isinstance(i, House):
                a_t_sum = a_t_sum + i.att_t

        # calculate probability of move to each house
        move_list = []
        for i in neighbors:
            if isinstance(i, House):
                move_dict = {}
                move_dict['house'] = (i.x_point, i.y_point)
                move_dict['prob'] = i.att_t / a_t_sum
                move_list.append(move_dict)

        # bubble sort the houses
        for i in range(len(move_list) - 1, 0, -1):
            for j in range(i):
                if move_list[j]['prob'] > move_list[j + 1]['prob']:
                    temp = move_list[j]
                    move_list[j] = move_list[j + 1]
                    move_list[j + 1] = temp
        # now decide what house you'll move to
        p = random.random()

        for row in move_list:
            if p < row['prob']:
                move_dest = row['house']
                self.model.grid.move_agent(self, pos=move_dest)

    def step(self):
        self.burgle_decision()
        if self.decision == 1:
            loc_contents = self.model.grid.get_cell_list_contents([(self.x_point, self.y_point)])
            for i in loc_contents:
                if isinstance(i, House):
                    i.burgle()
                    self.model.kill_agents.append(self)
        else:
            self.move()
