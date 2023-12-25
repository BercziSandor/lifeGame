from typing import Set

import numpy as np

from lifeGame.creatures.creature import Creature
from lifeGame.storyBoard import StoryBoard


class Simulation():
    time: float

    def __init__(self, step_hours: float = 1.0, storyBoard: StoryBoard = None,
                 duration_years: float = 2.0):
        self.step_hours = step_hours
        self.storyBoard = storyBoard
        self.duration_hours: float = duration_years * 365 * 24
        self.time = 0.0

        c: Creature
        for c in self.storyBoard.creatures:
            if not c.age_hours:
                c.age_hours = 0.0
            if not c.time_of_birth:
                c.time_of_birth = self.time - c.age_hours
            if c.die_at_age_years:
                c.time_of_death = c.time_of_birth + (c.die_at_age_years * 24 * 365)

    def get_creatures(self) -> Set[Creature]:
        return self.storyBoard.creatures

    def start(self):
        for t in np.arange(0.0, float(self.duration_hours),
                           float(self.step_hours)):
            print(t)
