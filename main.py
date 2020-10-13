import model
import numpy as np
import matplotlib.pyplot as plt
from agent import House

model = model.BurglaryModel(100, 150, 150, 5, 0.07, 0.06, 5.6, 0.2)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for i in range(300):
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
    plt.imshow(crime_counts, interpolation = 'nearest')
    plt.colorbar()
    plt.show()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
