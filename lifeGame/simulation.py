import numpy as np

from lifeGame.storyBoard import StoryBoard


class Simulation():
    def __init__(self, step_hours: float = 1, storyBoard: StoryBoard = None,
                 duration_years: float = 2):
        self.step_hours = step_hours
        self.storyBoard = storyBoard
        self.duration_hours: float = duration_years * 365 * 24

    def start(self):
        for t in np.arange(0.0, float(self.duration_hours),
                           float(self.step_hours)):
            print(t)
