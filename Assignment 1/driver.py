import os
from maze import Maze

def loadMazes():
    mazes = []

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    for i in range(50):
        file = "mazes/{}.txt".format(i)
        path = os.path.join(parent_dir, file)

        if os.path.exists(path):
            mazes.append(Maze.load(path))
        else:
            raise FileNotFoundError("Missing " + file)
    
    return mazes

# this should only be called once to generate 50 mazes if they are there do not use this again
def generateMazes():
    dir = os.path.dirname(os.path.abspath(__file__)) + "/mazes"
    mazes = []

    for i in range(50):
        mazes.append(Maze())
        path = dir + "/{}.txt".format(i)
        mazes[-1].save(path)

if __name__ == "__main__":
    mazes = loadMazes()
    mazes[0].display()