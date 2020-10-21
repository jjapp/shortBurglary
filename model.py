from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from agent import House, Criminal
import math
from statistics import mean, median
import random


def get_mean_att(model):
    att = [house.att_t for house in model.house_schedule.agents]
    return mean(att)


def get_max_att(model):
    att = [house.att_t for house in model.house_schedule.agents]
    return max(att)

def get_min_att(model):
    att = [house.att_t for house in model.house_schedule.agents]
    return min(att)


def get_num_criminals(model):
    return model.num_agents


class BurglaryModel(Model):

    def __init__(self, N, width, height, b_rate, delta, omega, theta, mu, gamma):
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

        a_0 = 0.2
        # place houses on grid, 1 house per grid location
        for i in range(self.width):
            for j in range(self.height):
                num = str(i) + str(j)
                num = int(num)
                a = House(num, self, a_0, i, j, self.delta, self.omega, self.theta, self.mu)
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
                             "Criminals": get_num_criminals})


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
    model = BurglaryModel(5, 100, 100, 2, 5, 5, 0.5, 0.2, 5)
    for i in range(10):
        model.step()

    print(model)
