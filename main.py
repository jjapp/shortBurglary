import model
import numpy as np
import matplotlib.pyplot as plt
from agent import House

model = model.BurglaryModel(150, 100, 100, 5, 0.01, 0.06, 0.56, 0.2, 0.02)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for i in range(100):
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
    plt.imshow(crime_counts, interpolation='nearest')
    plt.colorbar()
    plt.show()

    att = model.datacollector.get_model_vars_dataframe()
    att['Criminals'].plot()
    att.to_csv('model_stats.csv')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
