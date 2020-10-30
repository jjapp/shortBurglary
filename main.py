import model
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation
from agent import House

model = model.BurglaryModel(0, 128, 128, 5, 0.01, .06, 5.6, 0.1, 0.019, 1)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for i in range(1000):
        model.step()
        print(i)

    crime_counts = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        content, x, y = cell
        crimes = 0
        for row in content:
            if isinstance(row, House):
                crimes = row.att_t
                crime_counts[x][y] = crimes
    # make a color map of fixed colors
    cmap = colors.ListedColormap(['blue', 'white', 'green', 'red', 'yellow'])
    bounds = [0.2, 0.4, 1, 10]

    plt.imshow(crime_counts, interpolation='nearest', cmap=cmap)# cmap=plt.get_cmap('seismic'))
    plt.colorbar()
    plt.show()

    att = model.datacollector.get_model_vars_dataframe()
    houses = model.datacollector.get_agent_vars_dataframe()

    att.to_csv('model_stats.csv')
    houses.to_csv('houses.csv')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
