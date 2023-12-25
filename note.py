import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

Grid = np.zeros((10,10))
x = 0
y = 0

Grid[y,x] = 2
Grid[5,5] = -1

cmap = mpl.colors.ListedColormap(['green','white','red'])

def updateGrid(grid):
    grid = np.zeros((10,10))
    grid[5,5] = -1
    grid[0,0] = 2
    return grid

def _forward(x):
    return x


def _inverse(x):
    return x

def plot_grid(grid):
    norm = mpl.colors.FuncNorm((_forward, _inverse), vmin=-1, vmax=2)
    ax = plt.gca()

    # ax.invert_yaxis()
    ax.set_xticks(np.arange(0, 10, 1))
    # ax.set_yticks(np.arange(0, 10, 1))
    # ax.set_xticklabels(np.arange(0, 10, 1))
    # ax.set_yticklabels(np.arange(0, 10, 1))

    # ax.set_xticks(np.arange(-.5, 10, 1), minor=True)
    # ax.set_yticks(np.arange(-.5, 10, 1), minor=True)
    ax.imshow(grid,cmap=cmap,norm=norm,origin='lower')
    # Gridlines based on minor ticks
    ax.grid(which='minor', color='k', linestyle='-', linewidth=2)
    return ax

plt.ion()
fig = plot_grid(Grid)
plt.pause(1)
while True:
    fig.remove()
    Grid = updateGrid(Grid)
    fig = plot_grid(Grid)
    plt.pause(0.5)