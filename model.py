from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from agent import House, Criminal


class BurglaryModel(Model):

    def __init__(self, N, width, height, b_rate, delta, omega, theta, mu):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.width = width
        self.height = height
        self.houses = self.width * self.height
        self.schedule = SimultaneousActivation(self)
        self.b_rate = b_rate
        self.delta = delta
        self.omega = omega
        self.theta = theta
        self.mu = mu
        self.kill_agents = []

        a_0 = b_rate/delta
        # place houses on grid, 1 house per grid location
        for i in range(self.width):
            for j in range(self.height):
                num = str(i)+str(j)
                num = int(num)
                a = House(num, self, a_0, i, j, self.delta, self.omega, self.theta, self.mu)
                self.grid.place_agent(a, (a.x_point, a.y_point))
                # self.schedule.add(a)

        # place the criminals
        for k in range(self.num_agents):
            unique_id = "criminal"+str(k)
            criminal = Criminal(unique_id, self, self.width, self.height)
            self.grid.place_agent(criminal, (criminal.x_point, criminal.y_point))
            self.schedule.add(criminal)

    def step(self):
        # cycle through all houses and calculate updates on their attractiveness
        for i in range(self.width):
            for j in range(self.height):
                # get all agents at a location
                loc_contents = self.grid.get_cell_list_contents([(i, j)])
                for k in loc_contents:
                    if isinstance(k, House):
                        k.update_beta()
                        k.update_att()
                        k.update_p_s()
                        k.update_crime_list()
        self.schedule.step()


        '''
        for row in self.kill_agents:
            print (row.unique_id)

        
        for row in self.kill_agents:
            # self.grid.remove_agent(row)
            self.schedule.remove(row)
            self.kill_agents.remove(row)
            '''

if __name__ == '__main__':
    model = BurglaryModel(5, 100, 100, 2, 5, 5, 0.5, 0.2)
    for i in range(10):
        model.step()



    print (model)
