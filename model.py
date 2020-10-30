from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from agent import House, Criminal
import math
from statistics import mean, median
import random
import numpy as np


def get_mean_att(model):
    att = [house.att_t for house in model.house_schedule.agents]
    return median(att)


def get_max_att(model):
    att = [house.att_t for house in model.house_schedule.agents]
    return max(att)


def get_min_att(model):
    att = [house.att_t for house in model.house_schedule.agents]
    return min(att)


def get_num_criminals(model):
    return model.num_agents

def get_num_burgles(model):
    att = [house.crime_events for house in model.house_schedule.agents]
    return sum(att)


def get_att_map(model):
    # create numpy matrix
    crime_counts = np.zeros((model.grid.width, model.grid.height))

    for cell in model.grid.coord_iter():
        content, x, y = cell
        crimes = 0
        for row in content:
            if isinstance(row, House):
                crimes = row.att_t
                crime_counts[x][y] = crimes
    return crime_counts

def get_max_att_pos(model):
    max_pos=()
    max_att=0
    for row in model.house_schedule.agents:
        if row.att_t > max_att:
            max_pos = row.pos
            max_att = row.att_t
    return max_pos


class BurglaryModel(Model):

    def __init__(self, N, width, height, b_rate, delta, omega, theta, mu, gamma, space):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.width = width
        self.height = height
        self.houses = self.width * self.height
        self.schedule = SimultaneousActivation(self)
        self.house_schedule = SimultaneousActivation(self)
        self.b_rate = b_rate
        self.delta = delta
        self.omega = omega
        self.theta = theta
        self.mu = mu
        self.kill_agents = []
        self.gamma = gamma
        self.gen_agent = 1 - math.exp(-self.gamma*self.delta)
        self.total_agents = self.num_agents
        self.space = space

        a_0 = 0.2
        # place houses on grid, 1 house per grid location
        for i in range(self.width):
            for j in range(self.height):
                num = str(i) + str(j)
                num = int(num)
                a = House(num, self, a_0, i, j, self.delta, self.omega, self.theta, self.mu, self.space)
                self.grid.place_agent(a, (a.x_point, a.y_point))
                self.house_schedule.add(a)

        # place the criminals
        for k in range(self.num_agents):
            unique_id = "criminal" + str(k)
            criminal = Criminal(unique_id, self, self.width, self.height)
            self.grid.place_agent(criminal, (criminal.x_point, criminal.y_point))
            self.schedule.add(criminal)

        # set up data collection
        self.datacollector = DataCollector(
            model_reporters={"Mean_Attractiveness": get_mean_att,
                             "Max_Attractiveness": get_max_att,
                             "Min_Attractiveness": get_min_att,
                             "CrimeEvents": get_num_burgles,
                             "Criminals": get_num_criminals,
                             "MaxPos": get_max_att_pos},
            agent_reporters={"Att": lambda x: x.att_t if x.unique_id[:1]!="c" else None})


    def add_criminals(self):
        start_count = self.total_agents + 1
        for i in range(self.houses):
            y = random.random()
            if y < self.gen_agent:
                unique_id = "criminal" + str(start_count)
                criminal = Criminal(unique_id, self, self.width, self.height)
                self.grid.place_agent(criminal, (criminal.x_point, criminal.y_point))
                self.schedule.add(criminal)
                start_count = start_count + 1
                self.total_agents = start_count
                self.num_agents = self.num_agents + 1


    def step(self):
        self.datacollector.collect(self)
        # cycle through all houses and calculate updates on their attractiveness
        self.house_schedule.step()
        self.schedule.step()
        for row in self.kill_agents:
            try:
                self.grid.remove_agent(row)
                self.schedule.remove(row)
                self.kill_agents.remove(row)
                self.num_agents = self.num_agents - 1

            except:
                self.kill_agents.remove(row)

        # add new criminals

        self.add_criminals()


if __name__ == '__main__':
    model = BurglaryModel(5, 128, 128, 2, 5, 5, 5.6, 0.2, 5)
    for i in range(10):
        model.step()

    print(model)
